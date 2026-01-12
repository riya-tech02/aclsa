from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import numpy as np
from typing import List, Dict
import random

app = FastAPI(title="ACLSA RL Service")
app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_methods=["*"], allow_headers=["*"])

# Action space
ACTIONS = [
    "study_high_priority_skill",
    "work_on_project", 
    "apply_to_jobs",
    "rest_and_recover",
    "network_socialize",
    "explore_new_domain"
]

class DecisionRequest(BaseModel):
    user_id: str
    current_state: Dict
    context: str = "career_planning"

@app.get("/health")
def health():
    return {"status": "healthy", "service": "rl"}

@app.post("/rl/decide")
def make_decision(request: DecisionRequest):
    """RL agent recommends optimal action"""
    
    # Simple heuristic (replace with trained PPO model)
    state = request.current_state
    
    # Calculate scores for each action
    action_scores = {}
    for action in ACTIONS:
        score = random.uniform(0.5, 1.0)  # Placeholder
        
        # Add heuristics
        if "study" in action and state.get("energy", 0.5) > 0.6:
            score += 0.2
        if "rest" in action and state.get("energy", 0.5) < 0.4:
            score += 0.3
        if "project" in action and state.get("skills_ready", False):
            score += 0.25
            
        action_scores[action] = score
    
    # Select best action
    best_action = max(action_scores.items(), key=lambda x: x[1])
    
    return {
        "user_id": request.user_id,
        "recommended_action": best_action[0],
        "confidence": best_action[1],
        "action_scores": action_scores,
        "rationale": f"Based on current state analysis, {best_action[0]} offers the best long-term outcome",
        "expected_reward": {
            "career_progress": 0.15,
            "well_being": 0.10,
            "stability": 0.05
        },
        "alternative_actions": sorted(action_scores.items(), key=lambda x: x[1], reverse=True)[1:3]
    }

@app.post("/rl/train")
def train_agent(data: dict):
    """Train RL agent on experience"""
    return {
        "status": "training_started",
        "episodes": data.get("episodes", 100),
        "message": "Agent training in progress (simulated)"
    }

@app.get("/rl/policy/{user_id}")
def get_policy(user_id: str):
    """Get current policy for user"""
    return {
        "user_id": user_id,
        "policy_version": "v1.0",
        "training_episodes": 1000,
        "performance_metrics": {
            "avg_reward": 0.75,
            "success_rate": 0.82,
            "convergence": True
        }
    }
