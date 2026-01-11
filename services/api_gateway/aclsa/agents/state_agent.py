from aclsa.core.agent_base import AgentBase

class StateAgent(AgentBase):
    def __init__(self):
        super().__init__("StateAgent")

    def run(self, context):
        if "email" not in context.memory:
            context.state["needs_email"] = True
        return context
