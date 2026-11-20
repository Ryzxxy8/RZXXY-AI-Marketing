from config.settings import get_provider_config


class AIProvider:
    def __init__(self):
        self.config = get_provider_config()

    def get_info(self):
        return {
            "provider": self.config["api_key_env"],
            "model": self.config["model"] or "Not configured",
            "api_key_configured": bool(self.config["api_key"]),
            "base_url": self.config["base_url"],
        }


if __name__ == "__main__":
    provider = AIProvider()
    info = provider.get_info()

    print("AI Provider Configuration")
    print("--------------------------")
    print("Provider:", info["provider"])
    print("Model:", info["model"])
    print("API Key Configured:", info["api_key_configured"])
    print("Base URL:", info["base_url"])
