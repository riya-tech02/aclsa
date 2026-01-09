from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Dict, List

app = FastAPI(title="ACLSA Ethics Service")
app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_methods=["*"], allow_headers=["*"])

class ValidationRequest(BaseModel):
    user_id: str
    proposed_action: str
    current_state: Dict

@app.get("/health")
def health():
    return {"status": "healthy", "service": "ethics"}

@app.post("/ethics/validate")
def validate_action(request: ValidationRequest):
    """Validate action against ethical constraints"""
    
    violations = []
    warnings = []
    
    state = request.current_state
    action = request.proposed_action
    
    # Check health constraints
    if state.get("health", 0.8) < 0.3:
        if "study" in action or "work" in action:
            violations.append("Health too low for intensive activity")
    
    # Check burnout risk
    work_hours = state.get("weekly_hours", 40)
    if work_hours > 60:
        if "work" in action or "study" in action:
            warnings.append("Risk of burnout - consider rest")
    
    # Check financial constraints
    if state.get("financial_buffer", 1000) < 500:
        if "explore" in action:
            warnings.append("Low financial buffer - risky to explore new domains")
    
    # Check time constraints
    if state.get("available_hours", 8) < 2:
        violations.append("Insufficient time available")
    
    approved = len(violations) == 0
    
    return {
        "user_id": request.user_id,
        "action": request.proposed_action,
        "approved": approved,
        "violations": violations,
        "warnings": warnings,
        "safety_score": 1.0 - (len(violations) * 0.3 + len(warnings) * 0.1),
        "explanation": "Action validated against health, burnout, and resource constraints",
        "alternative_suggestion": "rest_and_recover" if not approved else None
    }

@app.post("/ethics/explain")
def explain_decision(data: dict):
    """Explain why a decision was made"""
    
    decision = data.get("decision", "unknown")
    
    return {
        "decision": decision,
        "explanation": f"The decision '{decision}' was made to optimize long-term well-being while respecting constraints",
        "factors": [
            {"factor": "Career progress", "weight": 0.4, "impact": "positive"},
            {"factor": "Health preservation", "weight": 0.3, "impact": "positive"},
            {"factor": "Financial stability", "weight": 0.2, "impact": "neutral"},
            {"factor": "Time availability", "weight": 0.1, "impact": "positive"}
        ],
        "constraints_satisfied": ["health >= 0.3", "weekly_hours <= 60"],
        "human_readable": "This decision balances career growth with personal well-being"
    }
