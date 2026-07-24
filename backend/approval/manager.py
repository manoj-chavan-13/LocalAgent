import uuid
from typing import Dict, Any

class ApprovalManager:
    """Manages explicit user approvals for safe mode."""
    
    def __init__(self):
        # In-memory store for pending actions. Real app uses DB/Redis.
        self.pending_actions: Dict[str, Dict[str, Any]] = {}

    def request_approval(self, action_type: str, details: dict) -> str:
        """Create a pending action and return its ID."""
        action_id = str(uuid.uuid4())
        self.pending_actions[action_id] = {
            "type": action_type,
            "details": details,
            "status": "pending"
        }
        return action_id

    def resolve_approval(self, action_id: str, approved: bool):
        if action_id in self.pending_actions:
            self.pending_actions[action_id]["status"] = "approved" if approved else "rejected"
            return True
        return False
        
approval_manager = ApprovalManager()
