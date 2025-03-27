from z3 import ModelRef

from definitions.evaluations.csp.parameters.cspParameters import CSPParameters
from testGeneration.modelValueExtractor import get_value_of_param


class ParameterModel:
    def __init__(self, model: ModelRef, csp_parameters: CSPParameters):
        self.parameter_dict = {}

        for param in model:
            if not csp_parameters.parameter_exists(str(param)):
                continue
            csp_param = csp_parameters[str(param)]
            self.parameter_dict[str(param)] = get_value_of_param(csp_parameters, param, model)
