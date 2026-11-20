import unittest
from unittest.mock import patch, Mock

from core.ai_engine import AIEngine


class TestAIEngine(unittest.TestCase):

    @patch("core.ai_engine.HTTPClient")
    @patch("core.ai_engine.load_knowledge")
    def test_generate(self, mock_knowledge, mock_client):
        mock_knowledge.return_value = (
            ["email"],
            "Marketing email knowledge"
        )

        mock_client.return_value.post.return_value = {
            "choices": [
                {
                    "message": {
                        "content": "Mock marketing email"
                    }
                }
            ]
        }

        engine = AIEngine()
        engine.config["api_key"] = "test-key"
        engine.config["model"] = "test-model"

        result = engine.generate("Write a marketing email")

        self.assertEqual(result["categories"], ["email"])
        self.assertEqual(result["answer"], "Mock marketing email")

        print("AI Engine Mock Test: PASSED")


if __name__ == "__main__":
    unittest.main()
