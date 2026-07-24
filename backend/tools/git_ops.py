from tools.base import BaseTool, ToolResult, registry
from tools.terminal import TerminalExecutionTool

class GitStatusTool(BaseTool):
    name = "git_status"
    description = "Get the current git status."
    parameters = {
        "type": "object",
        "properties": {
            "cwd": {"type": "string", "description": "Repository path"}
        },
        "required": []
    }

    async def execute(self, cwd: str = ".", **kwargs) -> ToolResult:
        term = TerminalExecutionTool()
        return await term.execute("git status", cwd=cwd)

class GitDiffTool(BaseTool):
    name = "git_diff"
    description = "Get git diff for the repository or a specific file."
    parameters = {
        "type": "object",
        "properties": {
            "filepath": {"type": "string", "description": "Specific file to diff, or empty for all."},
            "cwd": {"type": "string", "description": "Repository path"}
        },
        "required": []
    }

    async def execute(self, filepath: str = "", cwd: str = ".", **kwargs) -> ToolResult:
        cmd = f"git diff {filepath}" if filepath else "git diff"
        term = TerminalExecutionTool()
        return await term.execute(cmd, cwd=cwd)

registry.register(GitStatusTool())
registry.register(GitDiffTool())
