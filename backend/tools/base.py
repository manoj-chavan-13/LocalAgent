from abc import ABC, abstractmethod
from typing import Any, Dict, List
from pydantic import BaseModel

class ToolResult(BaseModel):
    success: bool
    output: str
    error: str = ""

class BaseTool(ABC):
    """Abstract base class for all tools."""
    
    @property
    @abstractmethod
    def name(self) -> str:
        pass
        
    @property
    @abstractmethod
    def description(self) -> str:
        pass

    @property
    @abstractmethod
    def parameters(self) -> Dict[str, Any]:
        """JSON schema defining the tool's input parameters."""
        pass

    @abstractmethod
    async def execute(self, **kwargs) -> ToolResult:
        """Executes the tool's logic and returns a ToolResult."""
        pass

class ToolRegistry:
    """Registry to manage and discover available tools."""
    
    def __init__(self):
        self._tools: Dict[str, BaseTool] = {}
        
    def register(self, tool: BaseTool):
        self._tools[tool.name] = tool
        
    def get_tool(self, name: str) -> BaseTool:
        return self._tools.get(name)
        
    def get_all_tools(self) -> List[BaseTool]:
        return list(self._tools.values())
        
registry = ToolRegistry()
