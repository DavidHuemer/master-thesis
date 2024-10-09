from definitions.evaluations.csp.parameters.resultParameters import ResultParameters


class ResultDto:
    def __init__(self, node, result_parameters: ResultParameters, result, result_verifier):
        self.node = node
        self.result_parameters = result_parameters
        self.result = result
        from verification.resultVerification.resultVerifier import ResultVerifier
        self.result_verifier: ResultVerifier = result_verifier

    def copy_with_other_node(self, node):
        return ResultDto(node=node,
                         result_parameters=self.result_parameters,
                         result=self.result, result_verifier=self.result_verifier)
