from z3 import ModelRef

from definitions.evaluations.csp.parameters.cspParameters import CSPParameters
from definitions.parameters.parameters import Parameters
from testGeneration.modelValueExtractor import get_value_of_param


class ParameterModel:
    def __init__(self, model: ModelRef, parameters: Parameters):
        self.parameter_dict = {}

        # for param in parameters:


        for model_param in model:
            if not parameters.exists(str(model_param)):
                continue
            param = parameters[str(model_param)]

            if model[param.get_state().csp_parameter.is_null_param]:
                self.parameter_dict[str(model_param)] = None
                continue

            self.parameter_dict[str(model_param)] = get_value_of_param(parameters, model_param, model)
