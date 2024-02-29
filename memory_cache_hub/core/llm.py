import requests
from typing import List
from dataclasses import asdict
from memory_cache_hub.core.types import Message

# TODO move this file to core/ollama.py

def ollama_completions(server_url: str, model: str, messages: List[Message]) -> str:
    """Send the prompt to the LLM server and return the response."""
    response = requests.post(
        server_url,
        json={
            "model": model,
            "stream": False,
            "messages": [asdict(message) for message in messages]
        }
    )
    response.raise_for_status()
    return response.json()["message"]["content"]


def openai_compatible_completions(server_url: str, model: str, messages: List[Message]) -> str:
    """Send the prompt to the OpenAI server and return the response."""
    response = requests.post(
        server_url,
        json={
            "model": model,
            "stream": False,
            "messages": [asdict(message) for message in messages]
        }
    )
    response.raise_for_status()
    return response.json()["choices"][0]["message"]["content"]
