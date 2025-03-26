from definitions.evaluations.BaseDto import BaseDto
from definitions.evaluations.csp.parameters.baseParameters import BaseParameters


class BaseExecutionDto(BaseDto):
    def __init__(self, node, parameters: BaseParameters, result):
        super().__init__(node)
        self.parameters = parameters
        self.result = result
