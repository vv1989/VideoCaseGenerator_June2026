import requests
from infrastructure.llm.base_llm import BaseLLM


class OpenAILLM(BaseLLM):
    def __init__(self, api_key, base_url=None):
        self.api_key = api_key

        self.base_url = (
            base_url
            or "https://generativelanguage.googleapis.com/v1beta/openai"
        )

    def generate(self, prompt):
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json",
        }

        payload = {
            "model": "gemini-2.5-flash",
            "messages": [
                {
                    "role": "user",
                    "content": prompt
                }
            ]
        }

        r = requests.post(
            ## f"{self.base_url}/chat/completions",
            f"{self.base_url}",
            json=payload,
            headers=headers,
            timeout=120
        )

        if r.status_code != 200:
            raise Exception(
                f"API Error {r.status_code}: {r.text}"
            )

        return r.json()["choices"][0]["message"]["content"]