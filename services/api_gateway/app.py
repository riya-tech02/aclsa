from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from aclsa.brain.supervisor import handle_message

app = FastAPI(title="ACLSA AGENT API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/message")
def message(user_id: str, text: str):
    return {"response": handle_message(user_id, text)}

@app.get("/health")
def health():
    return {"status": "agent_running"}
