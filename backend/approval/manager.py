import questionary
from rich.console import Console

console = Console()

class ApprovalManager:
    """Manages explicit user approvals for safe mode via CLI prompts."""
    
    def __init__(self):
        pass

    async def wait_for_approval(self, action_type: str, details: str) -> bool:
        """Prompt the user in the terminal for approval."""
        console.print(f"\n[bold yellow]⚠️ AGENT ACTION PENDING APPROVAL ({action_type})[/bold yellow]")
        console.print(f"[dim]{details}[/dim]\n")
        
        # questionary can be awaited directly
        return await questionary.confirm("Allow this action?").ask_async()

approval_manager = ApprovalManager()
