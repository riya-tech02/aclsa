from aclsa.core.agent_base import AgentBase

class MemoryAgent(AgentBase):
    def __init__(self):
        super().__init__("MemoryAgent")
        self.store = {}

    def run(self, context):
        self.store.setdefault(context.user_id, []).append(context.input)
        context.memory = self.store[context.user_id]
        return context
