class PostRequestDTO:
    def __init__(self, data):
        self.topic = data.get("topic")
        self.model = data.get("model", "llama3:instruct")

    def validate(self):
        if not self.topic:
            return False, "Topic is required"
        return True, None