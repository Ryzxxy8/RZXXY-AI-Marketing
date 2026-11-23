import base64
import unittest
from unittest.mock import patch

from web.app import app


class TestWebAPISecurity(unittest.TestCase):
    def setUp(self):
        self.client = app.test_client()
        self.original = {
            key: app.config.get(key)
            for key in ("AUTH_ENABLED", "APP_USERNAME", "APP_PASSWORD", "ALLOWED_HOSTS")
        }
        app.config.update(
            TESTING=True,
            AUTH_ENABLED=False,
            APP_USERNAME="admin",
            APP_PASSWORD="",
            ALLOWED_HOSTS=set(),
            MAX_CONTENT_LENGTH=64 * 1024,
        )

    def tearDown(self):
        app.config.update(self.original)

    def test_security_headers_are_present(self):
        response = self.client.get("/")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.headers["X-Content-Type-Options"], "nosniff")
        self.assertEqual(response.headers["X-Frame-Options"], "DENY")
        self.assertIn("Content-Security-Policy", response.headers)

    def test_authentication_is_required_when_enabled(self):
        app.config.update(
            AUTH_ENABLED=True,
            APP_USERNAME="admin",
            APP_PASSWORD="correct-horse-battery",
        )
        response = self.client.get("/")
        self.assertEqual(response.status_code, 401)
        self.assertIn("WWW-Authenticate", response.headers)

    def test_valid_basic_authentication_is_accepted(self):
        app.config.update(
            AUTH_ENABLED=True,
            APP_USERNAME="admin",
            APP_PASSWORD="correct-horse-battery",
        )
        token = base64.b64encode(b"admin:correct-horse-battery").decode("ascii")
        response = self.client.get("/", headers={"Authorization": "Basic " + token})
        self.assertEqual(response.status_code, 200)

    def test_chat_requires_json(self):
        response = self.client.post("/api/chat", data="message=hello")
        self.assertEqual(response.status_code, 415)

    def test_chat_rejects_invalid_json(self):
        response = self.client.post(
            "/api/chat",
            data="{invalid",
            content_type="application/json",
        )
        self.assertEqual(response.status_code, 400)

    def test_chat_rejects_non_string_message(self):
        response = self.client.post(
            "/api/chat",
            json={"message": ["not", "a", "string"]},
        )
        self.assertEqual(response.status_code, 400)

    def test_chat_rejects_oversized_message(self):
        response = self.client.post(
            "/api/chat",
            json={"message": "x" * 12001},
        )
        self.assertEqual(response.status_code, 400)

    @patch("web.app.AIEngine")
    def test_provider_errors_are_not_exposed_to_client(self, mock_engine):
        mock_engine.return_value.generate.side_effect = RuntimeError(
            "secret provider detail"
        )
        response = self.client.post("/api/chat", json={"message": "hello"})
        self.assertEqual(response.status_code, 502)
        self.assertNotIn(b"secret provider detail", response.data)
        self.assertIn(b"could not complete", response.data)


if __name__ == "__main__":
    unittest.main()
