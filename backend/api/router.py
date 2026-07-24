from fastapi import APIRouter
from api.endpoints import chat, repository, approval

api_router = APIRouter()

api_router.include_router(chat.router, prefix="/chat", tags=["chat"])
api_router.include_router(repository.router, prefix="/repo", tags=["repository"])
api_router.include_router(approval.router, prefix="/approvals", tags=["approvals"])

@api_router.get("/health")
async def health_check():
    """
    Basic health check endpoint.
    """
    return {"status": "ok", "message": "Local AI DevOps Agent is running."}
