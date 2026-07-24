import aiohttp
import json
from loguru import logger
from typing import List, Dict, Any, AsyncGenerator
from config.settings import get_settings

settings = get_settings()

class OllamaClient:
    """Client for communicating with the Ollama Chat API."""
    
    def __init__(self):
        self.base_url = settings.OLLAMA_BASE_URL
        self.model = settings.OLLAMA_MAIN_MODEL

    async def chat(self, messages: List[Dict[str, str]], stream: bool = False) -> Any:
        url = f"{self.base_url}/api/chat"
        payload = {
            "model": self.model,
            "messages": messages,
            "stream": stream
        }

        try:
            async with aiohttp.ClientSession() as session:
                async with session.post(url, json=payload) as response:
                    if response.status != 200:
                        error_text = await response.text()
                        logger.error(f"Ollama chat error: {error_text}")
                        return None
                    
                    if stream:
                        return self._stream_generator(response)
                    else:
                        data = await response.json()
                        return data.get("message", {}).get("content", "")
        except Exception as e:
            logger.error(f"Failed to connect to Ollama: {e}")
            return None

    async def _stream_generator(self, response: aiohttp.ClientResponse) -> AsyncGenerator[str, None]:
        async for line in response.content:
            if line:
                try:
                    data = json.loads(line)
                    if "message" in data and "content" in data["message"]:
                        yield data["message"]["content"]
                except json.JSONDecodeError:
                    continue

ollama_client = OllamaClient()
