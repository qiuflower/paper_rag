# core/config.py

import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
# Embedding model config
EMBEDDING_MODEL_NAME = "sentence-transformers/all-MiniLM-L6-v2"
EMBEDDING_DIM = 384  # all-MiniLM-L6-v2 输出维度

# Chunking config
CHUNK_SIZE = 512  # tokens
CHUNK_OVERLAP = 50  # tokens，方便上下文衔接

# Vector store config
FAISS_INDEX_PATH = os.path.join("vector_store", "faiss_index.bin")
FAISS_META_PATH = os.path.join("vector_store", "meta.json")

# 知识图谱文件路径
KG_DIR = os.path.join(BASE_DIR, "kg_store")
KG_FILE = os.path.join(KG_DIR, "graph.ttl")

# Data source
DATA_DIR = "data"

# LLM API config
LLM_API_URL = "https://yunwu.ai/v1/chat/completions"
LLM_API_KEY = os.getenv("YUNWU_API_KEY", "sk-UXulx2ibD0BWdwTW6yFbsvtxoXoOOSPk2ZVCyV5dfv29xPhH")  # 通过环境变量注入

# Reranker model
RERANKER_MODEL_NAME = "cross-encoder/ms-marco-MiniLM-L-6-v2"

# Logging
LOG_LEVEL = "INFO"

# Other parameters
MAX_TURNS = 5  # 多轮对话最大轮数

