from definitions.evaluations.csp.parameters.baseParameters import BaseParameters


class LocalResultParameters(BaseParameters):
    def __init__(self):
        self.parameters = dict()

    def __setitem__(self, key, value):
        self.parameters[key] = value

    def pop(self, key):
        if self.parameter_exists(key):
            self.parameters.pop(key)

    def parameter_exists(self, key: str) -> bool:
        return key in self.parameters

    def get_parameter_by_key(self, key: str, use_old: bool, use_this: bool):
        return self.parameters[key]

    def clear(self):
        self.parameters.clear()
