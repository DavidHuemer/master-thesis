import uuid

from z3 import Bool

from definitions.evaluations.csp.cspParameter import CSPParameter
from definitions.evaluations.csp.parameters.baseParameters import BaseParameters
from definitions.evaluations.csp.parameters.cspParamHelperType import CSPParamHelperType


class CSPParameters(BaseParameters):
    """
    This class stores the parameters that are used for generating valid method parameters
    """

    def __init__(self):
        self.parameters: dict[str, CSPParameter] = dict()
        self.helper_parameters: dict[tuple[str, CSPParamHelperType], str] = dict()
        self.is_null_param = Bool(f"is_null_{uuid.uuid4()}")

    def add_csp_parameter(self, param: CSPParameter):
        if self.parameter_exists(param.name):
            raise Exception(f"Key {param.name} already exists in CSPParameters")

        self.parameters[param.name] = param

    def get_parameter_by_key(self, key: str, use_old: bool, use_this: bool):
        return self.parameters[key]

    def get_actual_parameters(self):
        """
        Returns all parameters that are not helper parameters
        :return: A list of all parameters that are not helper parameters
        """

        return self.parameters.values()

    def parameter_exists(self, parameter_key: str) -> bool:
        return parameter_key in self.parameters

    def __getitem__(self, key: str) -> CSPParameter:
        return self.parameters[key]

    def __setitem__(self, key: str, value: CSPParameter):
        self.parameters[key] = value

    def remove_parameter(self, key: str):
        if key in self.parameters:
            del self.parameters[key]
        else:
            raise KeyError(f"Key {key} not found in CSPParameters")
