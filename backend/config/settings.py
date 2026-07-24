from pydantic_settings import BaseSettings
from pydantic import Field
from functools import lru_cache

class Settings(BaseSettings):
    """
    Application Settings
    Loads configuration from environment variables or .env file.
    """
    # API Settings
    PROJECT_NAME: str = "Local AI DevOps Engineering Agent"
    API_V1_STR: str = "/api/v1"
    
    # Ollama LLM Settings
    OLLAMA_BASE_URL: str = Field(default="http://localhost:11434")
    OLLAMA_MAIN_MODEL: str = Field(default="qwen2.5-coder")
    OLLAMA_EMBED_MODEL: str = Field(default="nomic-embed-text")
    
    # Database Settings
    MONGODB_URI: str = Field(default="mongodb://localhost:27017")
    MONGODB_DB_NAME: str = Field(default="local_agent_db")
    
    # ChromaDB Settings
    CHROMA_PERSIST_DIRECTORY: str = Field(default="./.chroma")
    
    # Safe Mode
    REQUIRE_APPROVAL_FOR_FILE_MODS: bool = Field(default=True)
    REQUIRE_APPROVAL_FOR_TERMINAL: bool = Field(default=True)

    class Config:
        env_file = ".env"
        case_sensitive = True

@lru_cache()
def get_settings() -> Settings:
    return Settings()
