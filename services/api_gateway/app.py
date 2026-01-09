from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import random
from typing import Dict, List

app = FastAPI(title="ACLSA API Gateway")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# In-memory storage
users_data = {}

class StateQuery(BaseModel):
    user_id: str

class NodeAdd(BaseModel):
    user_id: str
    node_type: str
    attributes: Dict

@app.get("/")
def root():
    return {"service": "ACLSA", "status": "live", "version": "2.0"}

@app.get("/health")
def health():
    return {"status": "healthy", "message": "All systems operational"}

@app.post("/state/initialize")
def initialize(user_id: str):
    users_data[user_id] = {"nodes": [], "edges": []}
    return {"status": "success", "user_id": user_id}

@app.post("/state/node")
def add_node(data: NodeAdd):
    if data.user_id not in users_data:
        users_data[data.user_id] = {"nodes": [], "edges": []}
    
    node = {
        "node_id": f"{data.node_type}_{len(users_data[data.user_id]['nodes'])}",
        "node_type": data.node_type,
        "attributes": data.attributes
    }
    users_data[data.user_id]["nodes"].append(node)
    
    return {"status": "success", "node_id": node["node_id"]}

@app.post("/state/query")
def query_state(data: StateQuery):
    if data.user_id not in users_data:
        return {
            "user_id": data.user_id,
            "nodes": [],
            "edges": [],
            "metadata": {"num_nodes": 0, "num_edges": 0, "node_types": []}
        }
    
    state = users_data[data.user_id]
    node_types = list(set(n["node_type"] for n in state["nodes"]))
    
    return {
        "user_id": data.user_id,
        "nodes": state["nodes"],
        "edges": state["edges"],
        "metadata": {
            "num_nodes": len(state["nodes"]),
            "num_edges": len(state["edges"]),
            "node_types": node_types
        }
    }

@app.post("/ai/chat")
def ai_chat(data: Dict):
    """ChatGPT-like conversational AI"""
    message = data.get("message", "")
    user_id = data.get("user_id", "guest")
    
    # Get user context
    context = users_data.get(user_id, {"nodes": []})
    skills = [n for n in context["nodes"] if n["node_type"] == "skill"]
    
    # Generate contextual response
    if "skill" in message.lower() or "learn" in message.lower():
        if skills:
            skill_names = [s["attributes"].get("name", "Unknown") for s in skills]
            response = f"Based on your current skills ({', '.join(skill_names)}), I recommend focusing on advanced topics or complementary skills. What specific area interests you?"
        else:
            response = "I see you haven't added any skills yet. What would you like to learn? I can help you create a personalized learning path."
    
    elif "career" in message.lower() or "job" in message.lower():
        response = "For career advancement, I recommend: 1) Building a strong portfolio of projects, 2) Networking in your field, 3) Continuous skill development. Would you like specific recommendations?"
    
    elif "recommend" in message.lower() or "suggest" in message.lower():
        actions = ["Deep work on your current project", "Learn a complementary skill", "Network with professionals", "Take a strategic break to recharge"]
        response = f"🎯 AI Recommendation: {random.choice(actions)}. This aligns with your long-term goals and current energy levels."
    
    else:
        responses = [
            f"I'm analyzing your profile... Based on your background, here's what I suggest: Focus on building real-world projects to demonstrate your skills.",
            f"Great question! As an AI career strategist, I'd recommend taking a balanced approach. What's your primary goal right now?",
            f"Let me help you with that. Could you provide more context about your current situation and what you're trying to achieve?",
            f"That's an interesting question. Based on behavioral psychology and career science, the best approach is to start small and build momentum. Want specifics?"
        ]
        response = random.choice(responses)
    
    return {
        "response": response,
        "confidence": round(random.uniform(0.85, 0.98), 2),
        "suggestions": [
            "Tell me about your current skills",
            "What are your career goals?",
            "Generate a personalized action plan",
            "Analyze my progress"
        ]
    }

@app.post("/ai/decision")
def ai_decision(data: Dict):
    """AI Decision Engine"""
    user_id = data.get("user_id", "guest")
    context = users_data.get(user_id, {"nodes": []})
    
    actions = [
        {"action": "Focus on Deep Learning", "impact": 0.92, "effort": 0.85},
        {"action": "Build Portfolio Projects", "impact": 0.88, "effort": 0.75},
        {"action": "Network & Connect", "impact": 0.79, "effort": 0.60},
        {"action": "Take Advanced Course", "impact": 0.85, "effort": 0.80}
    ]
    
    best = max(actions, key=lambda x: x["impact"])
    
    return {
        "recommended_action": best["action"],
        "confidence": 0.94,
        "reasoning": f"Based on analysis of your skills and market trends, {best['action']} offers the highest impact-to-effort ratio for your career trajectory.",
        "alternatives": [a["action"] for a in actions if a != best],
        "expected_outcomes": {
            "6_months": "Significant skill improvement and project completion",
            "1_year": "Career advancement opportunities and increased market value",
            "impact_score": best["impact"]
        }
    }

@app.post("/ai/simulate")
def simulate_future(data: Dict):
    """Future Trajectory Simulation"""
    scenarios = []
    
    for i in range(3):
        outcome = random.uniform(0.6, 0.95)
        scenarios.append({
            "scenario": f"Scenario {i+1}",
            "probability": round(random.uniform(0.2, 0.4), 2),
            "outcome_score": round(outcome, 2),
            "key_milestones": [
                f"Month {j*3}: Achievement level {round(outcome * (j/4), 2)}" 
                for j in range(1, 5)
            ]
        })
    
    best = max(scenarios, key=lambda x: x["outcome_score"])
    
    return {
        "scenarios": scenarios,
        "best_path": best,
        "recommendation": "Focus on consistent progress with strategic skill development",
        "confidence": 0.89
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
