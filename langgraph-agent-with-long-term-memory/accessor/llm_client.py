from typing import Any, Dict, List, Optional

try:
    from openai import OpenAI
except ImportError:
    OpenAI = None


DEFAULT_MODEL = "gpt-4.1"


def build_openai_client(api_key: Optional[str]):
    if OpenAI is None:
        raise RuntimeError(
            "The OpenAI Python SDK is not installed. Run: pip install openai"
        )
    if not api_key or api_key == "YOUR_API_KEY":
        raise RuntimeError(
            "OPENAI_API_KEY is not set. Export it or pass --openai-key."
        )
    return OpenAI(api_key=api_key)


def build_response_input(messages: List[Dict[str, str]]) -> List[Dict[str, Any]]:
    return [
        {
            "role": message["role"],
            "content": message["content"],
        }
        for message in messages
    ]
