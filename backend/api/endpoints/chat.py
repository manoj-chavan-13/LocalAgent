from fastapi import APIRouter
from pydantic import BaseModel
from fastapi.responses import StreamingResponse
from agent.loop import AgentLoop
import uuid

router = APIRouter()

class ChatRequest(BaseModel):
    message: str
    session_id: str = None

@router.post("/message")
async def chat_message(req: ChatRequest):
    session_id = req.session_id or str(uuid.uuid4())
    loop = AgentLoop(session_id)
    
    async def response_generator():
        async for chunk in loop.run(req.message):
            yield chunk
            
    return StreamingResponse(response_generator(), media_type="text/plain")
