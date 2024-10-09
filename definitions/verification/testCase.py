from definitions.evaluations.csp.parameters.methodCallParameters import MethodCallParameters


class TestCase:
    def __init__(self, parameters: MethodCallParameters):
        self.parameters = parameters

    def __str__(self):
        return f"Parameters: {self.parameters}"
