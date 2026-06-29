import os
import requests

from app.infrastructure.text.base_llm import BaseLLM


class TextLLM(BaseLLM):

    PROVIDERS = {

        "openai": {
            "base_url": "https://api.openai.com/v1",
            "model": "gpt-5",
            "env_key": "OPENAI_API_KEY"
        },

        "deepseek": {
            "base_url": "https://api.deepseek.com",
            "model": "deepseek-chat",
            "env_key": "DEEPSEEK_API_KEY"
        },

        "gemini": {
            "base_url": "https://generativelanguage.googleapis.com/v1beta/openai",
            "model": "gemini-2.5-flash",
            "env_key": "GEMINI_API_KEY"
        },

        "groq": {
            "base_url": "https://api.groq.com/openai/v1",
            "model": "llama-3.3-70b-versatile",
            "env_key": "GROQ_API_KEY"
        }
    }

    # ==================================================
    # INIT
    # ==================================================

    def __init__(
        self,
        provider,
        api_key=None,
        model=None,
        temperature=0.7,
        timeout=120,
        debug=True
    ):

        if provider not in self.PROVIDERS:

            raise ValueError(
                f"Unsupported provider: {provider}"
            )

        config = self.PROVIDERS[provider]

        self.provider = provider

        self.api_key = (
            api_key
            or os.getenv(
                config["env_key"]
            )
        )

        if not self.api_key:

            raise ValueError(
                f"Missing API key for {provider}. "
                f"Expected environment variable: "
                f"{config['env_key']}"
            )

        self.base_url = config["base_url"]

        self.model = (
            model
            or config["model"]
        )

        self.temperature = temperature

        self.timeout = timeout

        self.debug = debug

        if self.debug:

            print(
                f"🤖 TextLLM initialized"
            )

            print(
                f"🔧 Provider: {self.provider}"
            )

            print(
                f"🧠 Model: {self.model}"
            )

    # ==================================================
    # GENERATE
    # ==================================================

    def generate(
        self,
        prompt
    ):

        if self.debug:

            print(
                f"\n🚀 Calling {self.provider}"
            )

        headers = {

            "Authorization":
                f"Bearer {self.api_key}",

            "Content-Type":
                "application/json"
        }

        payload = {

            "model":
                self.model,

            "messages": [

                {
                    "role": "user",
                    "content": prompt
                }

            ],

            "temperature":
                self.temperature
        }

        response = requests.post(

            f"{self.base_url}/chat/completions",

            headers=headers,

            json=payload,

            timeout=self.timeout
        )

        if response.status_code != 200:

            raise Exception(

                f"\n❌ API Error\n"
                f"Provider: {self.provider}\n"
                f"Status: {response.status_code}\n"
                f"Response: {response.text}"
            )

        data = response.json()

        return data[
            "choices"
        ][0][
            "message"
        ][
            "content"
        ]

    # ==================================================
    # INFO
    # ==================================================

    def __repr__(self):

        return (
            f"TextLLM("
            f"provider={self.provider}, "
            f"model={self.model})"
        )

