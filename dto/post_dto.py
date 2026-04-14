class PostRequestDTO:
    def __init__(self, data):
        self.topic = data.get("topic")
        self.model = data.get("model", "phi3:latest")
        self.style = data.get("style", "professional")

    def validate(self):
        if not self.topic:
            return False, "Topic is required"
        return True, None