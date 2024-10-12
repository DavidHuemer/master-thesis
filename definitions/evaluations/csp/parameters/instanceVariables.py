from definitions.evaluations.csp.parameters.baseParameters import BaseParameters


class InstanceVariables(BaseParameters):
    def __init__(self):
        self.parameters = dict()

    def parameter_exists(self, key: str) -> bool:
        return key in self.parameters

    def get_parameter_by_key(self, key: str, use_old: bool, use_this: bool):
        return self.parameters[key]
