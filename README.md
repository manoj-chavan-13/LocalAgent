# Local AI DevOps Engineering Agent

A production-quality Local AI DevOps Engineering Agent, completely self-hosted using Ollama.

## Architecture Overview

- **Frontend**: React, TypeScript, TailwindCSS (Vite)
- **Backend**: Python 3.12+, FastAPI, AsyncIO
- **Database**: MongoDB (Local, via Motor async driver) for memory & metadata
- **LLM Engine**: Ollama API (Models: Qwen2.5-Coder, DeepSeek, etc.)
- **Vector DB**: ChromaDB (for codebase semantic search & embeddings)
- **Agent System**: Planner -> Tool Selector -> Executor -> Memory Loop

## Setup Instructions

### Prerequisites
- Python 3.12+
- Node.js 18+
- Ollama
- MongoDB
- Git

### Backend Setup
```bash
cd backend
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
pip install -r requirements.txt
uvicorn app:app --reload
```

### Frontend Setup
```bash
cd frontend
npm install
npm run dev
```
