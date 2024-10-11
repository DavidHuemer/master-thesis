from definitions.evaluations.BaseDto import BaseDto
from definitions.evaluations.csp.parameters.baseParameters import BaseParameters
from nodes.baseNodeRunner import BaseNodeRunner


class BaseExecutionDto(BaseDto):
    def __init__(self, node, parameters: BaseParameters, runner: BaseNodeRunner, result):
        super().__init__(node, runner)
        self.parameters = parameters
        self.result = result
