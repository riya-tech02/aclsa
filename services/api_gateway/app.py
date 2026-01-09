from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import httpx
from typing import Dict

app = FastAPI(title="ACLSA API Gateway", description="Unified interface for all ACLSA services")
app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_methods=["*"], allow_headers=["*"])

# Service URLs
SERVICES = {
    "state": "http://state_service:8001",
    "memory": "http://memory_service:8002",
    "planning": "http://planning_service:8003",
    "rl": "http://rl_service:8004",
    "ethics": "http://ethics_service:8005"
}

@app.get("/health")
async def health():
    """Health check for all services"""
    health_status = {}
    
    async with httpx.AsyncClient(timeout=5.0) as client:
        for name, url in SERVICES.items():
            try:
                response = await client.get(f"{url}/health")
                health_status[name] = "healthy" if response.status_code == 200 else "unhealthy"
            except:
                health_status[name] = "unreachable"
    
    all_healthy = all(status == "healthy" for status in health_status.values())
    
    return {
        "gateway": "healthy",
        "services": health_status,
        "overall": "healthy" if all_healthy else "degraded"
    }

@app.post("/decision/recommend")
async def recommend_decision(data: dict):
    """Get AI recommendation for user decision"""
    
    user_id = data["user_id"]
    
    async with httpx.AsyncClient(timeout=10.0) as client:
        # Get current state
        state_response = await client.post(
            f"{SERVICES['state']}/state/query",
            json={"user_id": user_id}
        )
        current_state = state_response.json()
        
        # Get RL recommendation
        rl_response = await client.post(
            f"{SERVICES['rl']}/rl/decide",
            json={
                "user_id": user_id,
                "current_state": {"energy": 0.7, "skills_ready": True},
                "context": data.get("context", "career_planning")
            }
        )
        recommendation = rl_response.json()
        
        # Validate with ethics
        ethics_response = await client.post(
            f"{SERVICES['ethics']}/ethics/validate",
            json={
                "user_id": user_id,
                "proposed_action": recommendation["recommended_action"],
                "current_state": {"health": 0.8, "weekly_hours": 45, "financial_buffer": 2000, "available_hours": 6}
            }
        )
        validation = ethics_response.json()
        
        return {
            "user_id": user_id,
            "recommendation": recommendation,
            "validation": validation,
            "final_decision": recommendation["recommended_action"] if validation["approved"] else validation.get("alternative_suggestion"),
            "explanation": validation["explanation"]
        }

@app.post("/analytics/simulate")
async def simulate_future(data: dict):
    """Simulate future trajectories"""
    
    async with httpx.AsyncClient(timeout=15.0) as client:
        response = await client.post(
            f"{SERVICES['planning']}/planning/simulate",
            json={
                "user_id": data["user_id"],
                "horizon_days": data.get("horizon_days", 90),
                "num_simulations": data.get("num_simulations", 100)
            }
        )
        return response.json()

@app.get("/")
def root():
    return {
        "service": "ACLSA API Gateway",
        "version": "1.0.0",
        "endpoints": {
            "health": "/health",
            "decision": "/decision/recommend",
            "simulate": "/analytics/simulate",
            "docs": "/docs"
        }
    }
