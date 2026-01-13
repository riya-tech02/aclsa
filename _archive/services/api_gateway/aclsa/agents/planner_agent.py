from aclsa.core.agent_base import AgentBase

class PlannerAgent(AgentBase):
    def __init__(self):
        super().__init__("PlannerAgent")

    def run(self, context):
        context.plan = [
            "understand_problem",
            "check_missing_info",
            "solve",
            "respond"
        ]
        return context
