from definitions.evaluations.csp.parameters.baseParameters import BaseParameters
from definitions.evaluations.csp.parameters.cspParameters import CSPParameters
from definitions.evaluations.csp.parameters.resultParameters import ResultParameters


class RangeParameters(BaseParameters):
    def __init__(self, result_parameters: ResultParameters, csp_parameters: CSPParameters):
        super().__init__()
        self.result_parameters = result_parameters
        self.csp_parameters = csp_parameters

    def parameter_exists(self, key: str) -> bool:
        return self.csp_parameters.parameter_exists(key) or self.result_parameters.parameter_exists(key)

    def get_parameter_by_key(self, key: str, use_old: bool, use_this: bool):
        if use_old or use_this:
            return self.csp_parameters.get_parameter_by_key(key, use_old, use_this)

        if self.csp_parameters.parameter_exists(key):
            return self.csp_parameters.get_parameter_by_key(key, use_old, use_this).value
        elif self.result_parameters.parameter_exists(key):
            return self.result_parameters.get_parameter_by_key(key, use_old, use_this)
