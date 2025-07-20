# paper_rag
多智能体学术文献智能问答系统

## 项目简介
paper_rag是一个多智能体混合检索系统，结合了 **向量检索（Dense Retrieval）**、**章节结构检索（Tree-based Retrieval）** 和 **知识图谱检索（KG Retrieval）**，并支持 **Cross-Encoder Reranker** 对候选结果进行重排，以提升检索精度与语义匹配效果。

## 项目亮点
- **三渠道融合**：向量检索 + 结构化章节匹配 + 知识图谱检索，有效提高查询覆盖率。
- **智能重排 (Reranker)**：可选用 `sentence-transformers` 的 Cross-Encoder 模型进行相关性重排。
- **高性能向量检索**：基于 `FAISS` 实现的高维向量索引和快速相似度计算。
- **结构化章节搜索**：通过 `TreeAgent` 提取并按文档结构进行匹配。
- **可扩展性**：可轻松接入新的检索通道或替换 Reranker 模型。
- **自动去重与多维排序**：通过去重策略和相似度/评分融合排序，提升最终结果质量。

## 功能模块
1. **FusionAgent**  
   - 实现多通道融合搜索。  
   - 支持 Reranker 重排候选结果。  

2. **retriever_agent**  
   - 基于 `sentence-transformers` 或其他模型生成文本向量。  
   - 使用 FAISS 进行高效检索。  

3. **TreeAgent**  
   - 支持按 Markdown/章节结构进行关键词搜索。  

4. **KGAgent**（可选）  
   - 基于实体关系的图谱搜索。
