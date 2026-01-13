from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime
import uuid

app = FastAPI(title="ACLSA Memory Service")
app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_methods=["*"], allow_headers=["*"])

# In-memory storage (replace with Qdrant in production)
memories = {}

class Memory(BaseModel):
    user_id: str
    content: str
    memory_type: str
    importance: float = 0.5

@app.get("/health")
def health():
    return {"status": "healthy", "service": "memory"}

@app.post("/memory/store")
def store_memory(memory: Memory):
    memory_id = str(uuid.uuid4())
    memories[memory_id] = {
        "id": memory_id,
        "user_id": memory.user_id,
        "content": memory.content,
        "memory_type": memory.memory_type,
        "importance": memory.importance,
        "timestamp": datetime.utcnow().isoformat()
    }
    return {"status": "success", "memory_id": memory_id}

@app.post("/memory/retrieve")
def retrieve_memories(data: dict):
    user_id = data["user_id"]
    query = data.get("query", "")
    
    user_memories = [m for m in memories.values() if m["user_id"] == user_id]
    user_memories.sort(key=lambda x: x["importance"], reverse=True)
    
    return {"memories": user_memories[:5], "count": len(user_memories)}

@app.get("/memory/stats/{user_id}")
def get_stats(user_id: str):
    user_memories = [m for m in memories.values() if m["user_id"] == user_id]
    return {
        "total": len(user_memories),
        "by_type": {},
        "avg_importance": sum(m["importance"] for m in user_memories) / max(len(user_memories), 1)
    }
