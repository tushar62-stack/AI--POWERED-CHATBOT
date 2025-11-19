import os
from pathlib import Path

from dotenv import load_dotenv


BASE_DIR = Path(__file__).resolve().parent
ENV_PATH = BASE_DIR / ".env"

if ENV_PATH.exists():
    load_dotenv(ENV_PATH)


def get_env_setting(key: str, default: str | None = None) -> str | None:
    """Fetch an environment variable with an optional default fallback."""
    return os.environ.get(key, default)


HUGGINGFACE_API_KEY = get_env_setting("HUGGINGFACE_API_KEY")

