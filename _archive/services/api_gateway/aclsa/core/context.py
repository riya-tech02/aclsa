class Context:
    def __init__(self, user_id, input_text):
        self.user_id = user_id
        self.input = input_text
        self.memory = {}
        self.state = {}
        self.plan = None
        self.response = None
