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

            # Parse tool calls from response (mocked here, real implementation would parse JSON blocks)
            # If no tools, break loop
            if "{" not in response: # naive check
                break
                
            # If tools were parsed, execute them and append to messages as 'system' or 'tool'
            # messages.append({"role": "user", "content": f"Tool Output: {result.output}"})
            break # Break for now to avoid infinite loop in stub
