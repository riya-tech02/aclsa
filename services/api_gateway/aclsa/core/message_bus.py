class MessageBus:
    def __init__(self):
        self.events = []

    def emit(self, sender, message):
        self.events.append({"from": sender, "message": message})

    def fetch(self):
        events = self.events[:]
        self.events.clear()
        return events
