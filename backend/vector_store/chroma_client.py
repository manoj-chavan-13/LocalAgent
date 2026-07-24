import chromadb
from loguru import logger
from config.settings import get_settings

settings = get_settings()

class ChromaClient:
    def __init__(self):
        self.client = chromadb.PersistentClient(path=settings.CHROMA_PERSIST_DIRECTORY)
        self.collection_name = "repository_index"
        logger.info(f"Initialized ChromaDB at {settings.CHROMA_PERSIST_DIRECTORY}")

    def get_or_create_collection(self):
        return self.client.get_or_create_collection(
            name=self.collection_name,
            metadata={"hnsw:space": "cosine"}
        )

    def add_documents(self, ids: list[str], documents: list[str], metadatas: list[dict], embeddings: list[list[float]]):
        """Add chunks of code to ChromaDB with their embeddings."""
        collection = self.get_or_create_collection()
        collection.upsert(
            ids=ids,
            documents=documents,
            metadatas=metadatas,
            embeddings=embeddings
        )
        logger.info(f"Upserted {len(ids)} documents into ChromaDB.")

    def search(self, query_embedding: list[float], n_results: int = 5):
        """Semantic search using query embedding."""
        collection = self.get_or_create_collection()
        results = collection.query(
            query_embeddings=[query_embedding],
            n_results=n_results
        )
        return results

chroma_db = ChromaClient()
