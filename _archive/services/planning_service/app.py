from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import numpy as np
from typing import List, Dict
import random

app = FastAPI(title="ACLSA Planning Service")
app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_methods=["*"], allow_headers=["*"])

class PlanRequest(BaseModel):
    user_id: str
    horizon_days: int = 90
    num_simulations: int = 100

@app.get("/health")
def health():
    return {"status": "healthy", "service": "planning"}

@app.post("/planning/simulate")
def simulate_trajectories(request: PlanRequest):
    """Run Monte Carlo simulations for future trajectories"""
    
    trajectories = []
    
    for sim in range(min(request.num_simulations, 10)):  # Limit for demo
        trajectory = {
            "simulation_id": sim,
            "days": request.horizon_days,
            "events": []
        }
        
        # Simulate random events
        current_skill = 0.5
        for day in range(0, request.horizon_days, 7):  # Weekly steps
            action = random.choice(["study", "project", "rest"])
            
            if action == "study":
                current_skill += random.uniform(0.01, 0.05)
            elif action == "project":
                current_skill += random.uniform(0.02, 0.08)
            else:
                current_skill += random.uniform(0, 0.01)
            
            trajectory["events"].append({
                "day": day,
                "action": action,
                "skill_level": min(current_skill, 1.0)
            })
        
        trajectory["final_skill"] = min(current_skill, 1.0)
        trajectory["success_probability"] = min(current_skill, 1.0)
        trajectories.append(trajectory)
    
    # Calculate statistics
    final_skills = [t["final_skill"] for t in trajectories]
    
    return {
        "user_id": request.user_id,
        "num_simulations": len(trajectories),
        "trajectories": trajectories[:3],  # Return top 3
        "statistics": {
            "mean_outcome": np.mean(final_skills),
            "std_outcome": np.std(final_skills),
            "best_case": max(final_skills),
            "worst_case": min(final_skills),
            "median": np.median(final_skills)
        },
        "recommendation": "Focus on consistent study for best outcomes"
    }

@app.post("/planning/counterfactual")
def counterfactual_analysis(data: dict):
    """What-if analysis"""
    scenario = data.get("scenario", "study_more")
    
    outcomes = {
        "study_more": {"skill_gain": 0.3, "time_cost": 200, "success_rate": 0.85},
        "do_projects": {"skill_gain": 0.4, "time_cost": 300, "success_rate": 0.75},
        "balanced": {"skill_gain": 0.35, "time_cost": 250, "success_rate": 0.80}
    }
    
    return {
        "scenario": scenario,
        "outcome": outcomes.get(scenario, outcomes["balanced"]),
        "comparison": "This scenario shows balanced risk-reward"
    }
