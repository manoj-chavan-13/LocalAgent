import aiohttp
from loguru import logger
from config.settings import get_settings

settings = get_settings()

class OllamaEmbedder:
    """Uses Ollama API to generate embeddings for text."""
    
    def __init__(self):
        self.base_url = settings.OLLAMA_BASE_URL
        self.model = settings.OLLAMA_EMBED_MODEL

    async def get_embedding(self, text: str) -> list[float]:
        """Generate an embedding for a single string using Ollama."""
        url = f"{self.base_url}/api/embeddings"
        payload = {
            "model": self.model,
            "prompt": text
        }
        try:
            async with aiohttp.ClientSession() as session:
                async with session.post(url, json=payload) as response:
                    if response.status == 200:
                        data = await response.json()
                        return data.get("embedding", [])
                    else:
                        error_text = await response.text()
                        logger.error(f"Ollama embedding failed: {error_text}")
                        return []
        except Exception as e:
            logger.error(f"Error communicating with Ollama embedding API: {e}")
            return []

    async def get_embeddings(self, texts: list[str]) -> list[list[float]]:
        """Generate embeddings for multiple strings concurrently."""
        import asyncio
        tasks = [self.get_embedding(text) for text in texts]
        return await asyncio.gather(*tasks)

embedder = OllamaEmbedder()
