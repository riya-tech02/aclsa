from aclsa.core.agent_base import AgentBase

class EthicsAgent(AgentBase):
    def __init__(self):
        super().__init__("EthicsAgent")

    def run(self, context):
        if "hack" in context.input.lower():
            context.response = "I can’t help with that."
        return context
