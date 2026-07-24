from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from approval.manager import approval_manager

router = APIRouter()

class ResolveRequest(BaseModel):
    approved: bool

@router.get("/pending")
async def get_pending_approvals():
    pending = approval_manager.get_pending()
    # Strip out the event object before returning JSON
    safe_pending = []
    for p in pending:
        safe_pending.append({
            "id": p["id"],
            "type": p["type"],
            "details": p["details"],
            "status": p["status"]
        })
    return {"pending": safe_pending}

@router.post("/{action_id}/resolve")
async def resolve_approval(action_id: str, req: ResolveRequest):
    success = approval_manager.resolve_approval(action_id, req.approved)
    if not success:
        raise HTTPException(status_code=404, detail="Action ID not found or already resolved.")
    return {"message": "Approval resolved successfully."}
