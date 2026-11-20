import unittest
from unittest.mock import patch, Mock

from core.http_client import HTTPClient


class TestHTTPClient(unittest.TestCase):

    @patch("core.http_client.requests.post")
    def test_post_request(self, mock_post):
        expected = {"message": "success"}

        mock_response = Mock()
        mock_response.json.return_value = expected
        mock_response.raise_for_status.return_value = None
        mock_post.return_value = mock_response

        client = HTTPClient(
            base_url="https://example.com/v1",
            api_key="test-key"
        )

        result = client.post(
            "/chat/completions",
            {"model": "test-model"}
        )

        self.assertEqual(result, expected)
        mock_post.assert_called_once()

        print("HTTP Client Mock Test: PASSED")


if __name__ == "__main__":
    unittest.main()
