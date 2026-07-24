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
        
        # questionary is synchronous but can be run asynchronously
        import asyncio
        loop = asyncio.get_event_loop()
        
        def ask():
            return questionary.confirm("Allow this action?").ask()
            
        return await loop.run_in_executor(None, ask)

approval_manager = ApprovalManager()
