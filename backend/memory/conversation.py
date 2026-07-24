from typing import List, Dict
from datetime import datetime
from memory.mongodb_client import mongodb

class ConversationMemory:
    """Manages chat history using MongoDB."""
    
    def __init__(self, session_id: str):
        self.session_id = session_id
        self.collection = mongodb.get_collection("conversations")

    async def add_message(self, role: str, content: str):
        message = {
            "session_id": self.session_id,
            "role": role,
            "content": content,
            "timestamp": datetime.utcnow()
        }
        await self.collection.insert_one(message)

    async def get_history(self, limit: int = 50) -> List[Dict[str, str]]:
        cursor = self.collection.find({"session_id": self.session_id}).sort("timestamp", 1).limit(limit)
        history = []
        async for doc in cursor:
            history.append({
                "role": doc["role"],
                "content": doc["content"]
            })
        return history
