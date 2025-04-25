from definitions.evaluations.BaseDto import BaseDto
from definitions.parameters.Variables import Variables


class BaseExecutionDto(BaseDto):
    def __init__(self, node, variables: Variables, result):
        super().__init__(node)
        self.variables = variables
        self.result = result
