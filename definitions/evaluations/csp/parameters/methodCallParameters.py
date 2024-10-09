from definitions.evaluations.csp.parameters.baseParameters import BaseParameters


class MethodCallParameters(BaseParameters):
    def __init__(self):
        self.parameters = dict()

    def get_parameter_by_key(self, key):
        return self.parameters[key]

    def __setitem__(self, key, value):
        self.parameters[key] = value

    def parameter_exists(self, key: str) -> bool:
        return key in self.parameters

    def __str__(self):
        return str(self.parameters)
