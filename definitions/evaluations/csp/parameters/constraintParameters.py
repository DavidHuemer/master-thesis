from definitions.evaluations.csp.cspParameter import CSPParameter
from definitions.evaluations.csp.parameters.baseParameters import BaseParameters
from definitions.evaluations.csp.parameters.cspParameters import CSPParameters


class ConstraintParameters(BaseParameters):
    def __init__(self, csp_parameters: CSPParameters):
        super().__init__()
        self.csp_parameters = csp_parameters
        self.loop_parameters = CSPParameters()
        self.functions: list[str] = []

    def parameter_exists(self, key: str) -> bool:
        return self.loop_parameters.parameter_exists(key) or self.csp_parameters.parameter_exists(key)

    def get_parameter_by_key(self, key: str, use_old: bool, use_this: bool, use_csp: bool = False) -> CSPParameter:
        if use_this or use_this:
            raise Exception("\\old and \\this are not supported in constraint parameters")

        if self.loop_parameters.parameter_exists(key):
            return self.loop_parameters[key]
        elif self.csp_parameters.parameter_exists(key):
            return self.csp_parameters[key]

        raise Exception(f"Parameter {key} does not exist")
