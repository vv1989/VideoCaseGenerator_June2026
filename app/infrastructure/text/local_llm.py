
import requests
from infrastructure.llm.base_llm import BaseLLM

class LocalLLM(BaseLLM):
    def __init__(self, base_url):
        self.base_url = base_url

    def generate(self, prompt):
        response = requests.post(
            f"{self.base_url}/api/generate",
            json={
                "model": "llama3.1:8b",
                "prompt": prompt,
                "stream": False
            }
        )
        return response.json()["response"]

