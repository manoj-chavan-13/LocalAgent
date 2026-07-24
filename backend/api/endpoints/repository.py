from fastapi import APIRouter, BackgroundTasks
from pydantic import BaseModel
from indexing.repository_scanner import RepositoryScanner
from indexing.chunker import TextChunker
from embeddings.ollama_embed import embedder
from vector_store.chroma_client import chroma_db
from loguru import logger
import uuid

router = APIRouter()

class IndexRequest(BaseModel):
    repository_path: str

async def _index_repository(path: str):
    logger.info(f"Starting background index for {path}")
    scanner = RepositoryScanner(path)
    files = scanner.scan()
    chunker = TextChunker()
    
    all_chunks = []
    for f in files:
        content = scanner.read_file_content(f)
        if content:
            chunks = chunker.chunk_text(content, f)
            all_chunks.extend(chunks)

    # Process in batches
    batch_size = 10
    for i in range(0, len(all_chunks), batch_size):
        batch = all_chunks[i:i+batch_size]
        texts = [c["content"] for c in batch]
        embeddings = await embedder.get_embeddings(texts)
        
        ids = [str(uuid.uuid4()) for _ in batch]
        metadatas = [{"filepath": c["filepath"], "start_line": c["start_line"]} for c in batch]
        
        chroma_db.add_documents(ids, texts, metadatas, embeddings)
        
    logger.info("Repository indexing completed.")

@router.post("/index")
async def index_repository(req: IndexRequest, background_tasks: BackgroundTasks):
    background_tasks.add_task(_index_repository, req.repository_path)
    return {"message": "Indexing started in the background."}
