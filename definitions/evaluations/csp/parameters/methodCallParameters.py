from definitions.evaluations.csp.parameters.baseParameters import BaseParameters
from definitions.evaluations.csp.parameters.methodCallParameter import MethodCallParameter


class MethodCallParameters(BaseParameters):
    def __init__(self):
        self.parameters = dict[str, MethodCallParameter]()

    def get_original_values(self):
        return [param.old_value for param in self.parameters.values()]

    def update_parameters(self, new_values: list):
        for i, key in enumerate(self.parameters):
            self.parameters[key].new_value = new_values[i]

    def get_parameter_by_key(self, key: str, use_old: bool, use_this: bool):
        return self.parameters[key].new_value

    def __getitem__(self, key):
        return self.parameters[key]

    def __setitem__(self, key, value):
        self.parameters[key] = value

    def parameter_exists(self, key: str) -> bool:
        return key in self.parameters

    def keys(self):
        return self.parameters.keys()

    def __str__(self):
        return str(self.parameters.values())
