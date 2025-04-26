import threading

from definitions.evaluations.baseExecutinoDto import BaseExecutionDto
from definitions.parameters.Variables import Variables


class ResultDto(BaseExecutionDto):
    def __init__(self, node, variables: Variables, result, stop_event: threading.Event):
        super().__init__(node=node, variables=variables, result=result)
        self.stop_event = stop_event

    def copy_with_other_node(self, node):
        return ResultDto(node=node,
                         variables=self.get_result_parameters(),
                         result=self.result, stop_event=self.stop_event)

    def get_result_parameters(self) -> Variables:
        if not isinstance(self.variables, Variables):
            raise Exception("ResultDto: Parameters are not of type Variables")
        return self.variables
