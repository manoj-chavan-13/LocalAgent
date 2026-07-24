from typing import AsyncGenerator
from llm.ollama_client import ollama_client
from planner.strategy import Planner
from tools.base import registry
from memory.conversation import ConversationMemory
from loguru import logger

class AgentLoop:
    """Iterative reasoning loop (Observe -> Reason -> Act)."""

    def __init__(self, session_id: str):
        self.memory = ConversationMemory(session_id)
        self.planner = Planner()
        self.max_iterations = 5

    async def run(self, user_request: str) -> AsyncGenerator[str, None]:
        await self.memory.add_message("user", user_request)
        
        # 1. Planning phase
        # In a full implementation, we'd query ChromaDB for repo_context
        repo_context = "Repo has a FastAPI backend and React frontend."
        plan = await self.planner.generate_plan(user_request, repo_context)
        
        yield f"**Plan:**\n{plan}\n\n"
        await self.memory.add_message("assistant", f"Plan generated:\n{plan}")

        # 2. Execution Loop
        history = await self.memory.get_history()
        
        # Add system prompt with tools
        tools_info = [f"{t.name}: {t.description}" for t in registry.get_all_tools()]
        system_prompt = f"You are a DevOps Agent. You have these tools: {', '.join(tools_info)}. " \
                        f"Reply with a tool call in JSON format if needed, or reply with the final answer."
        
        messages = [{"role": "system", "content": system_prompt}] + history

        for i in range(self.max_iterations):
            response = await ollama_client.chat(messages, stream=False)
            if not response:
                yield "Error communicating with LLM."
                break

            await self.memory.add_message("assistant", response)
            yield response + "\n"
            messages.append({"role": "assistant", "content": response})

            # Check for tool call signature (naive JSON extraction for simple prompt)
            import json
            import re
            
            # Look for JSON block in response
            match = re.search(r"```json\s*(\{.*?\})\s*```", response, re.DOTALL)
            if not match:
                # Fallback to looking for generic curly braces
                match = re.search(r"(\{.*?\})", response, re.DOTALL)

            if not match:
                break # No tool call found, end reasoning loop
                
            try:
                tool_call = json.loads(match.group(1))
                tool_name = tool_call.get("tool")
                kwargs = tool_call.get("parameters", {})
                
                tool = registry.get_tool(tool_name)
                if not tool:
                    messages.append({"role": "user", "content": f"Error: Tool '{tool_name}' not found."})
                    continue
                    
                yield f"\n*[Executing Tool: {tool_name}]*\n"
                result = await tool.execute(**kwargs)
                
                result_str = f"Tool output:\n{result.output}"
                if not result.success:
                    result_str = f"Tool failed:\n{result.error}"
                    
                messages.append({"role": "user", "content": result_str})
                
            except Exception as e:
                logger.error(f"Failed to parse tool call: {e}")
                messages.append({"role": "user", "content": f"Failed to parse your JSON tool call: {e}"})
