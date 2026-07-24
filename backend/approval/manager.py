import uuid
import asyncio
from typing import Dict, Any, Tuple

class ApprovalManager:
    """Manages explicit user approvals for safe mode."""
    
    def __init__(self):
        self.pending_actions: Dict[str, Dict[str, Any]] = {}

    def get_pending(self):
        return [
            {"id": k, **v} for k, v in self.pending_actions.items() if v["status"] == "pending"
        ]

    async def wait_for_approval(self, action_type: str, details: str) -> bool:
        """Create a pending action and block until approved or rejected."""
        action_id = str(uuid.uuid4())
        event = asyncio.Event()
        
        self.pending_actions[action_id] = {
            "type": action_type,
            "details": details,
            "status": "pending",
            "event": event
        }
        
        # Block until the event is set via API
        await event.wait()
        
        # Return boolean representing approval status
        is_approved = self.pending_actions[action_id]["status"] == "approved"
        # Cleanup
        del self.pending_actions[action_id]
        return is_approved

    def resolve_approval(self, action_id: str, approved: bool):
        if action_id in self.pending_actions:
            self.pending_actions[action_id]["status"] = "approved" if approved else "rejected"
            # Unblock the waiting tool
            self.pending_actions[action_id]["event"].set()
            return True
        return False
        
approval_manager = ApprovalManager()
