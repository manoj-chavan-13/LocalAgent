from motor.motor_asyncio import AsyncIOMotorClient
from loguru import logger
from typing import Optional
from config.settings import get_settings

settings = get_settings()

class MongoDBClient:
    def __init__(self):
        self.client: Optional[AsyncIOMotorClient] = None
        self.db = None

    async def connect(self):
        """Establish connection to MongoDB."""
        try:
            self.client = AsyncIOMotorClient(settings.MONGODB_URI)
            self.db = self.client[settings.MONGODB_DB_NAME]
            # Verify connection
            await self.client.admin.command('ping')
            logger.info("Successfully connected to MongoDB.")
        except Exception as e:
            logger.error(f"Failed to connect to MongoDB: {e}")
            raise e

    async def close(self):
        """Close connection to MongoDB."""
        if self.client:
            self.client.close()
            logger.info("MongoDB connection closed.")

    def get_collection(self, collection_name: str):
        """Get a specific collection from the database."""
        if self.db is None:
            raise Exception("Database not connected. Call connect() first.")
        return self.db[collection_name]

mongodb = MongoDBClient()
