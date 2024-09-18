class TestCase:
    def __init__(self, parameters: dict):
        self.parameters = parameters

    def __str__(self):
        return f"Parameters: {self.parameters}"
