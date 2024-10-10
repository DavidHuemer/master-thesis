from definitions.codeExecution.result.executionException import ExecutionException
from definitions.evaluations.csp.parameters.methodCallParameters import MethodCallParameters


class ExecutionResult:
    def __init__(self, result, parameters: MethodCallParameters, exception: ExecutionException | None = None):
        self.result = result
        self.parameters = parameters
        self.exception = exception

    def __str__(self):
        return f'Result: {self.result}, Parameters: {self.parameters}'
