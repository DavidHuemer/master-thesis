from definitions.evaluations.csp.parameters.cspParameters import CSPParameters
from definitions.evaluations.csp.parameters.instanceVariables import InstanceVariables

type InstanceVariables = InstanceVariables | None


class JmlParameters:
    def __init__(self, csp_parameters: CSPParameters):
        self.instance_variables: InstanceVariables = None
        self.old_instance_variables: InstanceVariables = None
        self.csp_parameters = csp_parameters
        self.functions: list[str] = []

    def get_parameter(self, key: str, use_old: bool = False, use_this: bool = False):
        pass

    def __getitem__(self, item):
        return self.__dict__[item]
