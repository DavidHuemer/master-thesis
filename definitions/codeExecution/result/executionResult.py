class ExecutionResult:
    def __init__(self, result, parameters, exception=None):
        self.result = result
        self.parameters = parameters
        self.exception = exception

    def __str__(self):
        return f'Result: {self.result}, Parameters: {self.parameters}'
