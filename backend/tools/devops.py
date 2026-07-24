from tools.base import BaseTool, ToolResult, registry
from tools.terminal import TerminalExecutionTool

class DockerComposeUpTool(BaseTool):
    name = "docker_compose_up"
    description = "Run docker-compose up -d in the specified directory."
    parameters = {
        "type": "object",
        "properties": {
            "cwd": {"type": "string", "description": "Directory containing docker-compose.yml"}
        },
        "required": ["cwd"]
    }

    async def execute(self, cwd: str, **kwargs) -> ToolResult:
        term = TerminalExecutionTool()
        return await term.execute("docker-compose up -d", cwd=cwd)

class TerraformPlanTool(BaseTool):
    name = "terraform_plan"
    description = "Run terraform plan in the specified directory."
    parameters = {
        "type": "object",
        "properties": {
            "cwd": {"type": "string", "description": "Directory containing terraform files"}
        },
        "required": ["cwd"]
    }

    async def execute(self, cwd: str, **kwargs) -> ToolResult:
        term = TerminalExecutionTool()
        return await term.execute("terraform plan", cwd=cwd)

registry.register(DockerComposeUpTool())
registry.register(TerraformPlanTool())
