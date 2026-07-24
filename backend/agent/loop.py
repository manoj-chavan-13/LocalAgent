import json
import re
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
        self.max_iterations = 10
        
    def _get_system_prompt(self, active_plan: str = None) -> str:
        tools = registry.get_all_tools()
        tools_schema = []
        for t in tools:
            tools_schema.append({
                "name": t.name,
                "description": t.description,
                "parameters": t.parameters
            })
            
        sys_prompt = (
            "You are an autonomous AI DevOps and Software Engineering Agent.\n"
            "You run in a loop of Thought, Action, Observation, and Answer.\n\n"
            "AVAILABLE TOOLS:\n"
            f"{json.dumps(tools_schema, indent=2)}\n\n"
            "RULES:\n"
            "1. You MUST ALWAYS start with a <thought> block to analyze the current state.\n"
            "2. If you need to take an action, output a single JSON block formatted exactly like this:\n"
            "```json\n"
            "{\n"
            "  \"tool\": \"tool_name\",\n"
            "  \"parameters\": {\"param1\": \"value1\"}\n"
            "}\n"
            "```\n"
            "3. After outputting the JSON tool call, STOP generating text. Wait for the Observation.\n"
            "4. If you have completed the task and no longer need tools, output a <thought> block explaining why, and then provide your final answer to the user in markdown format.\n"
            "5. If you do not know how to proceed, use the 'search_codebase' tool to query context.\n"
        )
        if active_plan:
            sys_prompt += f"\nACTIVE PLAN (Follow this step-by-step):\n{active_plan}\n"
            
        return sys_prompt
        
    async def run(self, user_prompt: str, active_plan: str = None) -> AsyncGenerator[str, None]:
        await self.memory.add_message("user", user_prompt)
        
        system_prompt = self._get_system_prompt(active_plan)
        
        for i in range(self.max_iterations):
            history = await self.memory.get_history()
            messages = [{"role": "system", "content": system_prompt}] + history
            
            yield f"\n\n**[Iteration {i+1}/{self.max_iterations}] Reasoning...**\n"
            
            response = await ollama_client.chat(messages, stream=False)
            if not response:
                yield "Error communicating with LLM."
                break

            await self.memory.add_message("assistant", response)
            
            # Print the thought process
            thought_match = re.search(r"<thought>(.*?)</thought>", response, re.DOTALL)
            if thought_match:
                yield f"\n*Thought: {thought_match.group(1).strip()}*\n"
            else:
                yield f"\n{response}\n"

            # Check for tool call signature
            match = re.search(r"```json\s*(\{.*?\})\s*```", response, re.DOTALL)
            if not match:
                # No JSON tool call, assume completion
                yield "\nTask completed or no further tools required.\n"
                break
                
            try:
                tool_call = json.loads(match.group(1))
                tool_name = tool_call.get("tool")
                kwargs = tool_call.get("parameters", {})
                
                tool = registry.get_tool(tool_name)
                if not tool:
                    err = f"Error: Tool '{tool_name}' not found."
                    yield f"\n{err}\n"
                    await self.memory.add_message("user", err)
                    continue
                    
                yield f"\n*[Executing Tool: {tool_name}]*\n"
                result = await tool.execute(**kwargs)
                
                result_str = f"Observation from {tool_name}:\n{result.output}"
                if not result.success:
                    result_str = f"Observation (ERROR) from {tool_name}:\n{result.error}"
                    
                await self.memory.add_message("user", result_str)
                
            except Exception as e:
                logger.error(f"Failed to parse tool call: {e}")
                await self.memory.add_message("user", f"System Error parsing JSON tool call: {e}")
