# agents/retriever_agent.py
import os
from utils.embedding import EmbeddingStore
from core.config import FAISS_INDEX_PATH, FAISS_META_PATH


class RetrieverAgent:
    def __init__(self):
        self.embedding_store = EmbeddingStore()
        # 判断是否已有索引文件，若有则加载
        if os.path.exists(FAISS_INDEX_PATH) and os.path.exists(FAISS_META_PATH):
            self.embedding_store.load()
        else:
            # 如果没有索引，则需要先构建索引
            # 这里留空或抛异常，建议由外部构建后调用load
            raise FileNotFoundError("FAISS index or meta file not found. Please build index first.")

    def retrieve(self, query, top_k=5):
        """
        根据用户查询进行向量检索，返回top_k最相关的文本块及距离
        返回格式：[(chunk_text, distance), ...]
        """
        if not self.embedding_store.index:
            raise ValueError("FAISS index is not loaded.")

        results = self.embedding_store.search(query, top_k=top_k)
        return results


#if __name__ == "__main__":
    #agent = RetrieverAgent()
    #results = agent.retrieve("示例查询")
    #for text, score in results:
        #print(f"Score: {score}, Text: {text[:100]}")
