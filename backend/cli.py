import asyncio
import questionary
from rich.console import Console
from rich.markdown import Markdown
from rich.panel import Panel
from rich.live import Live
import uuid
import sys
import os

from config.logging import setup_logging
from llm.ollama_client import ollama_client
from memory.mongodb_client import mongodb
from agent.loop import AgentLoop
import tools  # Register all tools

console = Console()

async def main():
    setup_logging()
    
    # 1. Connect to MongoDB
    console.print("[bold blue]Initializing Local AI DevOps Agent...[/bold blue]")
    try:
        await mongodb.connect()
    except Exception as e:
        console.print(f"[bold red]Failed to connect to MongoDB: {e}[/bold red]")
        sys.exit(1)
        
    # 2. Check Ollama Models
    with console.status("[cyan]Fetching available local models from Ollama..."):
        models = await ollama_client.get_available_models()
        
    if not models:
        console.print("[bold red]No models found! Please ensure Ollama is running and you have pulled at least one model (e.g. `ollama run qwen2.5-coder`).[/bold red]")
        sys.exit(1)
        
    # 3. Model Selection
    selected_model = await questionary.select(
        "Which model would you like to use?",
        choices=models
    ).ask_async()
    
    if not selected_model:
        sys.exit(0)
        
    ollama_client.set_model(selected_model)
    console.print(f"[green]Selected model: {selected_model}[/green]\n")
    
    # 4. Main REPL
    session_id = str(uuid.uuid4())
    console.print(Panel(
        f"[bold]Local Agent CLI[/bold]\nSession ID: {session_id}\nType 'exit' or 'quit' to close.",
        border_style="blue"
    ))
    
    agent = AgentLoop(session_id)
    
    while True:
        try:
            user_input = await questionary.text("You ❯").ask_async()
            if user_input is None or user_input.strip().lower() in ['exit', 'quit']:
                break
            if not user_input.strip():
                continue
                
            console.print("\n[bold cyan]Agent ❯[/bold cyan]")
            
            # Stream the response
            async for chunk in agent.run(user_input):
                # Using standard print to stream the raw markdown smoothly
                # Since Rich Live can sometimes be complex with partial markdown
                sys.stdout.write(chunk)
                sys.stdout.flush()
                
            print("\n")
            
        except KeyboardInterrupt:
            break
        except Exception as e:
            console.print(f"\n[bold red]Error in Agent Loop: {e}[/bold red]")
            
    # Cleanup
    await mongodb.close()
    console.print("\n[dim]Goodbye![/dim]")

if __name__ == "__main__":
    # Windows event loop policy fix for proper asyncio cleanup
    if sys.platform == 'win32':
        asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
    asyncio.run(main())
