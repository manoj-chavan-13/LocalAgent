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

    def set_model(self, model_name: str):
        """Dynamically set the model to be used."""
        self.model = model_name

    async def get_available_models(self) -> List[str]:
        """Fetch all models currently installed in the local Ollama instance."""
        url = f"{self.base_url}/api/tags"
        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(url) as response:
                    if response.status == 200:
                        data = await response.json()
                        return [m.get("name") for m in data.get("models", [])]
                    else:
                        logger.error(f"Failed to fetch models: {await response.text()}")
                        return []
        except Exception as e:
            logger.error(f"Failed to connect to Ollama: {e}")
            return []

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
