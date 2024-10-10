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
        self.is_null_helper_param: CSPParameter | None = None

    def add_csp_parameter(self, param: CSPParameter):
        if self.parameter_exists(param.name):
            raise Exception(f"Key {param.name} already exists in CSPParameters")

        self.parameters[param.name] = param

    def get_parameter_by_key(self, key: str, use_old: bool, use_this: bool):
        return self.parameters[key]

    def add_helper_parameter(self, parameter_key: str, helper_type: CSPParamHelperType, helper_param: CSPParameter):
        if self.parameter_exists(helper_param.name):
            raise Exception(f"Key {helper_param.name} already exists in CSPParameters")

        helper_tuple = (parameter_key, helper_type)
        if helper_tuple in self.helper_parameters:
            raise Exception(f"Helper parameter for key {parameter_key} and type {helper_type} already exists")

        self.helper_parameters[helper_tuple] = helper_param.name
        self.parameters[helper_param.name] = helper_param

    def get_actual_parameters(self):
        """
        Returns all parameters that are not helper parameters
        :return: A list of all parameters that are not helper parameters
        """

        keys = list(filter(lambda x: not self.parameters[x].is_helper, self.parameters.keys()))
        return [self.parameters[key] for key in keys]

    def get_helper(self, parameter_key: str, helper_type: CSPParamHelperType):
        helper_tuple = (parameter_key, helper_type)
        if helper_tuple not in self.helper_parameters:
            raise Exception(f"Helper parameter for key {parameter_key} and type {helper_type} does not exist")

        return self.parameters[self.helper_parameters[helper_tuple]]

    def get_helper_list_for_parameter(self, parameter_key: str) -> list[tuple[str, CSPParamHelperType]]:
        return list(filter(lambda x: x[0] == parameter_key, self.helper_parameters.keys()))

    def parameter_exists(self, parameter_key: str) -> bool:
        return parameter_key in self.parameters

    def __getitem__(self, key: str) -> CSPParameter:
        return self.parameters[key]

    def __setitem__(self, key: str, value: CSPParameter):
        self.parameters[key] = value
