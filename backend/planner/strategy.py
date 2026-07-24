from llm.ollama_client import ollama_client
from loguru import logger

class Planner:
    """Analyzes a user request and generates a step-by-step plan."""

    async def generate_plan(self, user_request: str, repo_context: str) -> str:
        prompt = f"""
You are an expert DevOps AI agent.
Analyze the user's request and the current repository context.
Generate a concrete, step-by-step plan using the tools available (file ops, git, terminal).

Repository Context:
{repo_context}

User Request:
{user_request}

Return ONLY the plan in bullet points.
"""
        messages = [{"role": "user", "content": prompt}]
        logger.info("Generating plan...")
        plan = await ollama_client.chat(messages, stream=False)
        logger.info("Plan generated.")
        return plan
