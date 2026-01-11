from aclsa.brain.dialog_state import get_state, set_state

# local imports instead of HTTP
from services.memory_service.app import store_memory
from services.planning_service.app import simulate_trajectories
from services.rl_service.app import make_decision

def handle_message(user_id: str, text: str):
    state = get_state(user_id)

    if state["phase"] == "NEW":
        set_state(user_id, "WAITING_EMAIL", ["email"])
        return "Before I continue, please share your email."

    if state["phase"] == "WAITING_EMAIL":
        if "@" in text:
            store_memory({
                "user_id": user_id,
                "content": text,
                "memory_type": "email",
                "importance": 1.0
            })
            set_state(user_id, "WAITING_GOAL", ["goal"])
            return "Thanks. What is your main goal?"
        return "Please provide a valid email."

    if state["phase"] == "WAITING_GOAL":
        store_memory({
            "user_id": user_id,
            "content": text,
            "memory_type": "goal",
            "importance": 0.9
        })

        plan = simulate_trajectories({
            "user_id": user_id,
            "horizon_days": 90
        })

        decision = make_decision({
            "user_id": user_id,
            "current_state": {
                "energy": 0.6,
                "skills_ready": True
            }
        })

        set_state(user_id, "DONE")

        return {
            "plan": plan,
            "recommended_action": decision
        }

    return "Processing..."

                       
