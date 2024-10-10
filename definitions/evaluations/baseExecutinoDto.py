from definitions.evaluations.csp.parameters.baseParameters import BaseParameters


class BaseExecutionDto:
    def __init__(self, parameters: BaseParameters, result):
        self.parameters = parameters
        self.result = result
