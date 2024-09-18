class ExecutionResult:
    def __init__(self, result, parameters):
        self.result = result
        self.parameters = parameters

    def __str__(self):
        return f'Result: {self.result}, Parameters: {self.parameters}'
