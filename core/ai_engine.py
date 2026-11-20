from core.knowledge_loader import load_knowledge
from core.ai_provider import AIProvider
from core.http_client import HTTPClient


class AIEngine:
    def __init__(self):
        self.provider = AIProvider()
        self.config = self.provider.config

    def generate(self, task):
        if not self.config["api_key"]:
            raise RuntimeError("AI API key is not configured.")

        if not self.config["model"]:
            raise RuntimeError("AI model is not configured.")

        categories, knowledge = load_knowledge(task)

        client = HTTPClient(
            base_url=self.config["base_url"],
            api_key=self.config["api_key"],
        )

        payload = {
            "model": self.config["model"],
            "messages": [
                {
                    "role": "system",
                    "content": (
                        "You are RZXXY AI Marketing Assistant. "
                        "Use the supplied marketing knowledge. "
                        "Provide clear, practical and ethical advice.\n\n"
                        + knowledge
                    ),
                },
                {
                    "role": "user",
                    "content": task,
                },
            ],
        }

        response = client.post("chat/completions", payload)

        return {
            "categories": categories,
            "answer": response["choices"][0]["message"]["content"],
        }
