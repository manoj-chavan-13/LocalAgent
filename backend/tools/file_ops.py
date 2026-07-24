import os
import shutil
from loguru import logger
from tools.base import BaseTool, ToolResult, registry
from config.settings import get_settings

settings = get_settings()

class ReadFileTool(BaseTool):
    name = "read_file"
    description = "Read the contents of a file at the given path."
    parameters = {
        "type": "object",
        "properties": {
            "filepath": {"type": "string", "description": "Absolute or relative path to the file."}
        },
        "required": ["filepath"]
    }

    async def execute(self, filepath: str, **kwargs) -> ToolResult:
        if not os.path.exists(filepath):
            return ToolResult(success=False, output="", error=f"File not found: {filepath}")
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                content = f.read()
            return ToolResult(success=True, output=content)
        except Exception as e:
            return ToolResult(success=False, output="", error=str(e))

class WriteFileTool(BaseTool):
    name = "write_file"
    description = "Write content to a file. Overwrites if it exists."
    parameters = {
        "type": "object",
        "properties": {
            "filepath": {"type": "string", "description": "Absolute or relative path to the file."},
            "content": {"type": "string", "description": "Content to write."}
        },
        "required": ["filepath", "content"]
    }

    async def execute(self, filepath: str, content: str, **kwargs) -> ToolResult:
        if settings.REQUIRE_APPROVAL_FOR_FILE_MODS:
            from approval.manager import approval_manager
            logger.warning(f"Modification to {filepath} pending approval...")
            details = f"Write to file: {filepath}\n\nContent excerpt:\n{content[:200]}..."
            approved = await approval_manager.wait_for_approval("write_file", details)
            if not approved:
                return ToolResult(success=False, output="", error="User rejected the file modification.")

        try:
            os.makedirs(os.path.dirname(os.path.abspath(filepath)), exist_ok=True)
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(content)
            return ToolResult(success=True, output=f"Successfully wrote to {filepath}")
        except Exception as e:
            return ToolResult(success=False, output="", error=str(e))

registry.register(ReadFileTool())
registry.register(WriteFileTool())
