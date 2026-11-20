import os
from pathlib import Path
from dotenv import load_dotenv

PROJECT_ROOT = Path(__file__).resolve().parent.parent

load_dotenv(PROJECT_ROOT / ".env")

PROVIDER = os.getenv("AI_PROVIDER", "gemini")

PROVIDERS = {
    "openai": {
        "base_url": "https://api.openai.com/v1",
        "api_key_env": "OPENAI_API_KEY",
    },
    "anthropic": {
        "base_url": "https://api.anthropic.com/v1",
        "api_key_env": "ANTHROPIC_API_KEY",
    },
    "gemini": {
        "base_url": "https://generativelanguage.googleapis.com/v1beta/openai",
        "api_key_env": "GEMINI_API_KEY",
    },
}


def get_provider_config():
    if PROVIDER not in PROVIDERS:
        raise ValueError("Unsupported provider: {}".format(PROVIDER))

    config = PROVIDERS[PROVIDER].copy()
    config["api_key"] = os.getenv(config["api_key_env"])
    config["model"] = os.getenv(
        "AI_MODEL",
        "gemini-3.5-flash-lite" if PROVIDER == "gemini" else ""
    )

    return config
