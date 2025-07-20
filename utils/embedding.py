import os
import faiss
import numpy as np
import json
from sentence_transformers import SentenceTransformer
from core.config import FAISS_INDEX_PATH, FAISS_META_PATH, EMBEDDING_MODEL_NAME

"""

EmbeddingStore class for managing embeddings and FAISS index.
This class allows building, saving, loading, and searching embeddings using FAISS.
加载预训练embedding模型;对文本 chunk 生成向量;构建 FAISS 索引并保存、加载
根据 query 进行向量搜索返回相关文本

"""
class EmbeddingStore:
    def __init__(self):
        self.model = SentenceTransformer(EMBEDDING_MODEL_NAME)
        self.index = None
        self.meta = []
        if os.path.exists(FAISS_INDEX_PATH) and os.path.exists(FAISS_META_PATH):
            self.load()

    def build_index(self, chunks, save=True):
        embeddings = self.model.encode(chunks, convert_to_numpy=True)
        dim = embeddings.shape[1]
        self.index = faiss.IndexFlatL2(dim)
        self.index.add(embeddings)
        self.meta = chunks
        if save:
            self._save()

    def search(self, query, top_k=5):
        if self.index is None:
            raise ValueError("FAISS index is not built or loaded.")
        query_vec = self.model.encode([query], convert_to_numpy=True)
        D, I = self.index.search(query_vec, top_k)
        results = []
        for i, idx in enumerate(I[0]):
            if idx < 0 or idx >= len(self.meta):
                continue
            results.append((self.meta[idx], float(D[0][i])))
        return results

    def _save(self):
        faiss.write_index(self.index, FAISS_INDEX_PATH)
        with open(FAISS_META_PATH, "w", encoding="utf-8") as f:
            json.dump(self.meta, f, ensure_ascii=False, indent=2)

    def _save(self):
        # 确保目录存在
        os.makedirs(os.path.dirname(FAISS_INDEX_PATH), exist_ok=True)
        os.makedirs(os.path.dirname(FAISS_META_PATH), exist_ok=True)

        faiss.write_index(self.index, FAISS_INDEX_PATH)
        with open(FAISS_META_PATH, "w", encoding="utf-8") as f:
            json.dump(self.meta, f, ensure_ascii=False, indent=2)

    def load(self):
        self.index = faiss.read_index(FAISS_INDEX_PATH)
        with open(FAISS_META_PATH, "r", encoding="utf-8") as f:
            self.meta = json.load(f)
