# agents/reasoning_agent_gpt.py
import requests
from core.config import LLM_API_URL, LLM_API_KEY

class ReasoningAgentGPT:
    def __init__(self):
        self.api_url = LLM_API_URL
        self.api_key = LLM_API_KEY

    def chat(self, messages):
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }
        payload = {
            "model": "gpt-4o-mini",
            "messages": messages
        }
        response = requests.post(self.api_url, headers=headers, json=payload)
        if response.status_code == 200:
            return response.json()
        else:
            raise Exception(f"LLM API Error: {response.status_code}, {response.text}")

if __name__ == "__main__":
    agent = ReasoningAgentGPT()
    messages = [{"role": "user", "content": "请简要介绍人工智能。"}]
    resp = agent.chat(messages)
    print(resp)
