from aclsa.agents.planner_agent import PlannerAgent
from aclsa.agents.memory_agent import MemoryAgent
from aclsa.agents.ethics_agent import EthicsAgent
from aclsa.agents.state_agent import StateAgent
from aclsa.agents.rl_agent import RLAgent

class SupervisorAgent:
    def __init__(self):
        self.memory = MemoryAgent()
        self.planner = PlannerAgent()
        self.ethics = EthicsAgent()
        self.state = StateAgent()
        self.rl = RLAgent()

    def run(self, context):
        context = self.memory.run(context)
        context = self.ethics.run(context)

        if context.response:
            return context.response

        context = self.state.run(context)

        if context.state.get("needs_email"):
            return "Before I continue, can you share your email?"

        context = self.planner.run(context)

        context.response = f"I understood your problem: '{context.input}'. I will solve it step by step."
        return context.response
