import asyncio
from loguru import logger
from tools.base import BaseTool, ToolResult, registry
from config.settings import get_settings

settings = get_settings()

class TerminalExecutionTool(BaseTool):
    name = "execute_command"
    description = "Execute a shell command. Use carefully."
    parameters = {
        "type": "object",
        "properties": {
            "command": {"type": "string", "description": "The command to run."},
            "cwd": {"type": "string", "description": "The directory to run the command in."}
        },
        "required": ["command"]
    }

    async def execute(self, command: str, cwd: str = ".", **kwargs) -> ToolResult:
        if settings.REQUIRE_APPROVAL_FOR_TERMINAL:
            from approval.manager import approval_manager
            logger.warning(f"Command execution pending approval: {command}")
            details = f"Execute command in {cwd}:\n\n> {command}"
            approved = await approval_manager.wait_for_approval("execute_command", details)
            if not approved:
                return ToolResult(success=False, output="", error="User rejected the terminal command.")

        try:
            process = await asyncio.create_subprocess_shell(
                command,
                stdout=asyncio.subprocess.PIPE,
                stderr=asyncio.subprocess.PIPE,
                cwd=cwd
            )
            stdout, stderr = await process.communicate()
            
            output = stdout.decode('utf-8').strip()
            error = stderr.decode('utf-8').strip()
            
            success = process.returncode == 0
            return ToolResult(
                success=success, 
                output=output, 
                error=error if not success else ""
            )
        except Exception as e:
            return ToolResult(success=False, output="", error=str(e))

registry.register(TerminalExecutionTool())
