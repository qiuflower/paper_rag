# agents/fusion_agent.py

from typing import List, Dict, Any, Optional
from utils.embedding import EmbeddingStore
from agents.tree_agent import TreeAgent
from core.config import RERANKER_MODEL_NAME

try:
    from sentence_transformers import CrossEncoder
except ImportError:
    CrossEncoder = None


class FusionAgent:
    """
    三通道混合检索：
      - Dense / Vector (EmbeddingStore + FAISS)
      - Tree / Structured Markdown Chapters (TreeAgent)
      - KG / Entity-Relation Context (KGAgent)
    可选：Cross-Encoder Reranker 对候选重排。
    """
    def __init__(self,
                 documents: Dict[str, str],
                 embedding_store: Optional[EmbeddingStore] = None,
                 tree_agent: Optional[TreeAgent] = None,
                 kg_agent: Optional[Any] = None,
                 use_reranker: bool = True):
        self.embedding_store = embedding_store or EmbeddingStore()
        self.tree_agent = tree_agent or TreeAgent(documents)
        self.kg_agent = kg_agent

        self.use_reranker = use_reranker and (CrossEncoder is not None)
        self._reranker_model = None
        if self.use_reranker:
            self._reranker_model = CrossEncoder(RERANKER_MODEL_NAME)

    def _vector_search(self, query: str, top_k: int = 5):
        try:
            return self.embedding_store.search(query, top_k=top_k)
        except Exception as e:
            print(f"[FusionAgent] 向量检索失败: {e}")
            return []

    def _tree_search(self, query: str, top_k: Optional[int] = None):
        results = self.tree_agent.search_by_heading(query)
        if top_k is not None:
            results = results[:top_k]
        return results

    def _kg_search(self, query: str, top_k: int = 5):
        if self.kg_agent is None:
            return []
        if hasattr(self.kg_agent, "search"):
            try:
                return self.kg_agent.search(query, top_k=top_k)
            except Exception as e:
                print(f"[FusionAgent] KG search失败: {e}")
                return []
        if hasattr(self.kg_agent, "query_neighbors"):
            neighbors = self.kg_agent.query_neighbors(query, depth=1)
            kg_results = []
            for n in neighbors[:top_k]:
                kg_results.append({
                    "subject": query,
                    "predicate": "related_to",
                    "object": n,
                    "text": f"{query} -> {n}"
                })
            return kg_results
        return []

    def hybrid_search(self,
                      query: str,
                      top_k: int = 5,            # 控制最终返回数量
                      top_k_vector: int = 5,
                      top_k_tree: int = 5,
                      top_k_kg: int = 5,
                      rerank_limit: int = 20) -> List[Dict[str, Any]]:
        """
        返回融合后的候选列表（可选rerank）。
        """
        # 1. 各通道检索
        vec_raw = self._vector_search(query, top_k=top_k_vector)  # [(text, dist), ...]
        tree_raw = self._tree_search(query, top_k=top_k_tree)     # [{'heading':..., 'content':...}, ...]
        kg_raw = self._kg_search(query, top_k=top_k_kg)           # [{'subject':..,'predicate':..,'object':..,'text':..}, ...]

        # 2. 统一结构化候选项
        candidates = []
        seen = set()

        for text, dist in vec_raw:
            norm_text = text.strip()
            if not norm_text or norm_text in seen:
                continue
            candidates.append({
                "source": "vector",
                "text": norm_text,
                "score": float(dist),
                "meta": {"distance": float(dist)}
            })
            seen.add(norm_text)

        for item in tree_raw:
            content = item.get("content", "").strip()
            heading = item.get("heading", "")
            if not content or content in seen:
                continue
            candidates.append({
                "source": "tree",
                "text": content,
                "score": None,
                "meta": {"heading": heading}
            })
            seen.add(content)

        for kg_item in kg_raw:
            txt = kg_item.get("text")
            if not txt:
                s = kg_item.get("subject", "")
                p = kg_item.get("predicate", "")
                o = kg_item.get("object", "")
                txt = f"{s} --{p}--> {o}"
            txt = str(txt).strip()
            if not txt or txt in seen:
                continue
            candidates.append({
                "source": "kg",
                "text": txt,
                "score": None,
                "meta": {
                    "subject": kg_item.get("subject"),
                    "predicate": kg_item.get("predicate"),
                    "object": kg_item.get("object")
                }
            })
            seen.add(txt)

        if not candidates:
            return []

        # 3. 可选：Reranker重排
        if self.use_reranker is not None:
            print("[FusionAgent] 使用Reranker进行重排...")
            if self._reranker_model is None:
                raise RuntimeError("Reranker模型未初始化，请检查配置。")
            to_rank = candidates[:rerank_limit]
            pairs = [(query, c["text"]) for c in to_rank]
            scores = self._reranker_model.predict(pairs)
            for c, s in zip(to_rank, scores):
                c["rerank_score"] = float(s)
            to_rank.sort(key=lambda x: x.get("rerank_score", 0.0), reverse=True)
            return to_rank[:top_k]

        # 4. 无reranker：按 fallback_score 排序，距离转相似度，Tree和KG给默认分数
        for c in candidates:
            if c["source"] == "vector":
                dist = c["meta"]["distance"]
                c["fallback_score"] = 1.0 / (1.0 + dist)
            else:
                c["fallback_score"] = 0.5
        candidates.sort(key=lambda x: x["fallback_score"], reverse=True)
        return candidates[:top_k]
