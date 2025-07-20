# main.py
import os
from utils.file_loader import load_markdown_files
from utils.embedding import EmbeddingStore
from agents.tree_agent import TreeAgent
from agents.kg_agent import KGAgent
from agents.fusion_agent import FusionAgent
from agents.reasoning_agent_gpt import ReasoningAgentGPT
from agents.orchestrator import Orchestrator
from core.config import FAISS_INDEX_PATH, FAISS_META_PATH, KG_FILE
from utils.markdown_parser import split_markdown_by_heading
from utils.kg_builder import KnowledgeGraph


def build_indexes(documents, embedding_store):
    print("开始构建向量索引...")
    from utils.markdown_parser import split_markdown_by_heading

    all_chunks = []
    for md_text in documents.values():
        chapters = split_markdown_by_heading(md_text, level=2)
        for ch in chapters:
            content = ch['content'].strip()
            if content:  # 过滤空块
                all_chunks.append(content)

    if not all_chunks:
        raise ValueError("没有可用的文本块，请检查Markdown文件是否有内容。")

    print(f"有效文本块数量: {len(all_chunks)}")
    embedding_store.build_index(all_chunks)
    print("向量索引构建完成。")

def build_kg(documents):
    print("开始构建知识图谱...")
    kg = KnowledgeGraph()
    for text in documents.values():
        kg.extract_triples(text)
    os.makedirs(os.path.dirname(KG_FILE), exist_ok=True)
    kg.save()
    print(f"知识图谱已保存到 {KG_FILE}")

def main():
    print("加载Markdown文档...")
    documents = load_markdown_files("data")
    print(f"共加载 {len(documents)} 个文档。")

    #print(f"加载到的Markdown keys: {list(documents.keys())}")
    #for name, content in documents.items():
        #print(f"文件 {name} 内容长度: {len(content)}")
        #print(f"文件内容预览: {content[:200]}")
    #for md_text in documents.values():
        #chapters = split_markdown_by_heading(md_text, level=2)
        #print(f"解析章节数量: {len(chapters)}")
        #for ch in chapters:
            #print(f"章节标题: {ch.get('title')}, 内容长度: {len(ch.get('content'))}")

    # 1. 初始化向量存储和索引
    embedding_store = EmbeddingStore()

    # 如果索引文件不存在，自动构建索引
    if not (os.path.exists(FAISS_INDEX_PATH) and os.path.exists(FAISS_META_PATH)):
        print("FAISS索引文件不存在，开始自动构建索引...")
        build_indexes(documents, embedding_store)
    else:
        embedding_store.load()
        print("加载已有向量索引。")

    # 2. 初始化TreeAgent和KGAgent
    if not os.path.exists(KG_FILE):
        print("知识图谱文件不存在，开始构建...")
        build_kg(documents)
    else:
        print("加载已有知识图谱。")

    # 3. 初始化融合Agent
    fusion_agent = FusionAgent(documents, use_reranker=True)
    fusion_agent.embedding_store = embedding_store

    # 4. 初始化ReasoningAgentGPT和Orchestrator
    # reasoning_agent = ReasoningAgentGPT()
    orchestrator = Orchestrator()

    print("系统初始化完成，进入交互模式。输入 exit 退出。")

    while True:
        user_input = input("你：").strip()
        if user_input.lower() in ("exit", "quit"):
            print("退出系统。")
            break
        answer = orchestrator.chat(user_input)
        print(f"助手：{answer}")

if __name__ == "__main__":
    main()
