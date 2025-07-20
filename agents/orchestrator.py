# agents/orchestrator.py
from agents.fusion_agent import FusionAgent
from agents.reasoning_agent_gpt import ReasoningAgentGPT
from utils.file_loader import load_markdown_files

class Orchestrator:
    def __init__(self):
        self.documents = load_markdown_files("data")
        self.fusion_agent = FusionAgent(self.documents)
        self.reasoning_agent = ReasoningAgentGPT()
        self.chat_history = []

    def chat(self, user_input):
        self.chat_history.append({"role": "user", "content": user_input})

        # 检索相关上下文
        retrieved = self.fusion_agent.hybrid_search(user_input, top_k=3)
        print(self.fusion_agent._reranker_model) 
        
        # 拼接参考文本，并标注来源索引
        context_text = "\n---\n".join([f"[参考文档段落 {i+1}]\n{r['text']}" for i, r in enumerate(retrieved)])

        # 构造 LLM prompt，明确告诉模型回答基于这些内容
        prompt = [
            {"role": "system", "content": "你是一个知识问答助理。请根据提供的参考内容回答问题，且说明回答基于哪些内容。"},
            *self.chat_history,
            {"role": "system", "content": f"参考文档内容：\n{context_text}"}
        ]

        # 调用 LLM
        resp = self.reasoning_agent.chat(prompt)
        answer = resp.get("choices", [{}])[0].get("message", {}).get("content", None)

        if not answer:
            answer = "抱歉，没有获取到回答。"
        else:
            # 额外拼接一句，说明回答是基于哪些参考内容
            answer += "\n\n[说明] 本回答依据以上参考文档段落内容生成。"

        self.chat_history.append({"role": "assistant", "content": answer})

        return answer


if __name__ == "__main__":
    orchestrator = Orchestrator()
    while True:
        query = input("用户输入: ")
        if query.lower() in ("exit", "quit"):
            break
        ans = orchestrator.chat(query)
        print(f"助手: {ans}")
