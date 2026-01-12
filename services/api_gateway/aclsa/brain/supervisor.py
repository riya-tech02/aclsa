import re
import httpx

MEMORY_URL = "http://memory:8002/memory/store"
PLANNING_URL = "http://planning:8003/planning/simulate"
RL_URL = "http://rl:8004/rl/decide"

SMALL_TALK = {
    "hi", "hii", "hello", "hey", "ok", "okay", "hmm", "thanks", "thank you"
}

EMAIL_REGEX = r"[^@]+@[^@]+\.[^@]+"

async def handle_message(user_id: str, text: str):
    t = text.lower().strip()

    # 1️⃣ SMALL TALK → CHAT ONLY
    if t in SMALL_TALK:
        return "Hello! How can I help you today?"

    # 2️⃣ EMAIL
    if re.fullmatch(EMAIL_REGEX, t):
        async with httpx.AsyncClient() as client:
            await client.post(
                MEMORY_URL,
                json={
                    "user_id": user_id,
                    "content": t,
                    "memory_type": "email",
                    "importance": 1.0
                }
            )
        return "Thanks. What is your main goal?"

    # 3️⃣ VERY SHORT INPUT
    if len(t.split()) < 3:
        return "Please tell me a bit more so I can help properly."

    # 4️⃣ FULL AGENT MODE (ONLY HERE)
    async with httpx.AsyncClient() as client:
        plan = await client.post(
            PLANNING_URL,
            json={"user_id": user_id, "horizon_days": 90}
        )
        decision = await client.post(
            RL_URL,
            json={
                "user_id": user_id,
                "current_state": {
                    "energy": 0.7,
                    "skills_ready": True
                }
            }
        )

    return {
        "summary": "I’ve analyzed your situation and created a plan with a recommended next action.",
        "plan": plan.json(),
        "decision": decision.json()
    }


                   
