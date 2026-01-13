from fastapi import FastAPI
from aclsa.agents.supervisor_agent import SupervisorAgent
from aclsa.core.context import Context

app = FastAPI()
brain = SupervisorAgent()

@app.post("/message")
def message(user_id: str, text: str):
    context = Context(user_id, text)
    reply = brain.run(context)
    return {"response": reply}
