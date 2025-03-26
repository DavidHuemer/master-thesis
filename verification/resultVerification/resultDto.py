import threading

from definitions.evaluations.baseExecutinoDto import BaseExecutionDto
from definitions.evaluations.csp.parameters.resultParameters import ResultParameters


class ResultDto(BaseExecutionDto):
    def __init__(self, node, result_parameters: ResultParameters, result, result_verifier, stop_event: threading.Event):
        super().__init__(node=node, parameters=result_parameters, result=result)
        from verification.resultVerification.resultVerifier import ResultVerifier
        self.result_verifier: ResultVerifier = result_verifier
        self.stop_event = stop_event

    def copy_with_other_node(self, node):
        return ResultDto(node=node,
                         result_parameters=self.get_result_parameters(),
                         result=self.result, result_verifier=self.result_verifier, stop_event=self.stop_event)

    def get_result_parameters(self) -> ResultParameters:
        if not isinstance(self.parameters, ResultParameters):
            raise Exception("ResultDto: Parameters are not of type ResultParameters")
        return self.parameters
