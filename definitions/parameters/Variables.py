from copy import copy

from definitions.parameters.parameter import Parameter
from definitions.parameters.parameters import Parameters
from definitions.parameters.specialParameters import SpecialParameters


class Variables:
    def __init__(self, method_call_parameters=None, special_parameters=None):
        self.method_call_parameters = method_call_parameters or Parameters()
        self.instance_parameters: Parameters = Parameters()
        self.loop_parameters: Parameters = Parameters()
        self.special_parameters = special_parameters or SpecialParameters()

    def add_method_call_parameter(self, param: Parameter):
        self.method_call_parameters.add_parameter(param)

    def exists(self, key: str):
        return self.method_call_parameters.exists(key) or \
            self.instance_parameters.exists(key) or \
            self.loop_parameters.exists(key)

    def get_variable_by_key(self, key: str, use_this: bool = False) -> Parameter:
        if use_this:
            return self.instance_parameters[key]

        if self.method_call_parameters.exists(key):
            return self.method_call_parameters[key]
        elif self.instance_parameters.exists(key):
            return self.instance_parameters[key]
        elif self.loop_parameters.exists(key):
            return self.loop_parameters[key]
        else:
            raise KeyError(f"Variable {key} not found in any parameters.")

    def get_method_call_visualization(self):
        return self.method_call_parameters.get_values_str(use_old=False)

    def __copy__(self):
        return Variables(
            method_call_parameters=copy(self.method_call_parameters),
            special_parameters=self.special_parameters
        )

    def __str__(self):
        return (f"Method Call Parameters: {str(self.method_call_parameters)}, "
                f"Instance Parameters: {str(self.instance_parameters)}, "
                f"Loop Parameters: {str(self.loop_parameters)}")
