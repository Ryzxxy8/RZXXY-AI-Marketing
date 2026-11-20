import requests


class HTTPClient:
    def __init__(self, base_url, api_key, timeout=30):
        self.base_url = base_url.rstrip("/")
        self.api_key = api_key
        self.timeout = timeout

    def post(self, endpoint, payload, headers=None):
        if not self.api_key:
            raise ValueError("API key is required.")

        request_headers = {
            "Content-Type": "application/json",
        }

        if self.api_key:
            request_headers["Authorization"] = (
                "Bearer {}".format(self.api_key)
            )

        if headers:
            request_headers.update(headers)

        response = requests.post(
            self.base_url + "/" + endpoint.lstrip("/"),
            json=payload,
            headers=request_headers,
            timeout=self.timeout,
        )

        response.raise_for_status()
        return response.json()
