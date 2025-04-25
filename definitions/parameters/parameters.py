from copy import copy
from os.path import join

from z3 import ModelRef, And

from definitions.parameters.parameter import Parameter


class Parameters:
    def __init__(self, parameters=None):
        self._parameters = parameters or dict()

    def add_parameter(self, param: Parameter):
        """
        Add a parameter to the parameters list
        :param param: Parameter to add
        :return: None
        """

        if self.exists(param.name):
            raise Exception(f"Parameter {param.name} already exists")

        self._parameters[param.name] = param

    def exists(self, key: str) -> bool:
        """
        Check if a parameter exists in the parameters list
        :param key: Parameter name to check
        :return: True if the parameter exists, False otherwise
        """
        return key in self._parameters.keys()

    def evaluate(self, model: ModelRef, use_old: bool = False):
        func_decl_dict = {
            str(func_decl): func_decl for func_decl in model
        }

        for param in self.get_parameter_list():
            param.evaluate(model, func_decl_dict, use_old)

    def get_parameter_list(self) -> list[Parameter]:
        """
        Get the list of parameters
        :return: List of parameters
        """
        return list(self._parameters.values())

    def get_constraints(self, use_old: bool = False) -> list:
        """
        Get the list of constraints
        :return: List of constraints
        """
        return [param.get_constraint(use_old) for param in self.get_parameter_list()]

    def get_and_constraints(self, use_old: bool = False):
        return And(*self.get_constraints(use_old))

    def remove_parameter(self, key: str):
        """
        Remove a parameter from the parameters list
        :param key: Parameter name to remove
        :return: None
        """
        if key in self._parameters:
            del self._parameters[key]
        else:
            raise KeyError(f"Key {key} not found in Parameters")

    def get_values_str(self, use_old: bool = False) -> list:
        """
        Get the values of the parameters as a string
        :return: String representation of the parameter values
        """
        return [param.get_state(use_old).parameter_value.python_value for param in self.get_parameter_list()]

    def __copy__(self):
        copied_parameters = {key: copy(param) for key, param in self._parameters.items()}
        return Parameters(copied_parameters)

    def __str__(self):
        return f"[{', '.join(str(param) for param in self._parameters.values())}]"

    def __iter__(self):
        return iter(self._parameters.values())

    def __getitem__(self, key: str) -> Parameter:
        return self._parameters[key]
