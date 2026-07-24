from typing import Dict, Any
from tools.base import BaseTool, ToolResult
from vector_store.chroma_client import chroma_client

class SearchCodebaseTool(BaseTool):
    """Tool for semantically searching the codebase using ChromaDB vector representations."""
    
    @property
    def name(self) -> str:
        return "search_codebase"
        
    @property
    def description(self) -> str:
        return "Perform semantic search across the indexed codebase to find relevant code snippets, functions, or documentation."
        
    @property
    def parameters(self) -> Dict[str, Any]:
        return {
            "type": "object",
            "properties": {
                "query": {
                    "type": "string",
                    "description": "The search query, e.g., 'Authentication logic', 'Database connection', 'How does the User model work?'"
                },
                "n_results": {
                    "type": "integer",
                    "description": "Number of results to return (default 5).",
                    "default": 5
                }
            },
            "required": ["query"]
        }

    async def execute(self, query: str, n_results: int = 5, **kwargs) -> ToolResult:
        try:
            results = chroma_client.search(query, n_results=n_results)
            
            if not results or not results['documents'] or len(results['documents'][0]) == 0:
                return ToolResult(success=True, output="No relevant code snippets found. Has the repository been indexed?")
                
            formatted_output = f"--- Search Results for '{query}' ---\n\n"
            
            for idx, doc in enumerate(results['documents'][0]):
                meta = results['metadatas'][0][idx]
                filepath = meta.get('filepath', 'Unknown File')
                
                formatted_output += f"File: {filepath}\n"
                formatted_output += "```\n"
                formatted_output += f"{doc}\n"
                formatted_output += "```\n"
                formatted_output += "-" * 40 + "\n"
                
            return ToolResult(success=True, output=formatted_output)
            
        except Exception as e:
            return ToolResult(success=False, output="", error=f"Vector search failed: {str(e)}")

from tools.base import registry
registry.register(SearchCodebaseTool())
