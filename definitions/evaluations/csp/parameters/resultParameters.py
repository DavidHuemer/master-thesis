from definitions.evaluations.csp.parameters.baseParameters import BaseParameters
from definitions.evaluations.csp.parameters.cspParameters import CSPParameters
from definitions.evaluations.csp.parameters.instanceVariables import InstanceVariables
from definitions.evaluations.csp.parameters.localResultParameters import LocalResultParameters
from definitions.evaluations.csp.parameters.methodCallParameters import MethodCallParameters


class ResultParameters(BaseParameters):
    """
    Parameters for result evaluation
    Containing the parameters which were used for calling the method.
    Does also contain the old and new instance of the class. (Old instance means before executing the method)
    """

    def __init__(self, old_instance_variables: InstanceVariables,
                 new_instance_variables: InstanceVariables,
                 method_call_parameters: MethodCallParameters,
                 csp_parameters: CSPParameters):
        self.local_parameters = LocalResultParameters()
        self.old_instance_variables = old_instance_variables
        self.new_instance_variables = new_instance_variables
        self.method_call_parameters = method_call_parameters
        self.csp_parameters = csp_parameters

    def parameter_exists(self, key: str) -> bool:
        return (self.local_parameters.parameter_exists(key) or
                self.method_call_parameters.parameter_exists(key) or
                self.new_instance_variables.parameter_exists(key) or
                self.old_instance_variables.parameter_exists(key))

    def get_parameter_by_key(self, key: str, use_old: bool, use_this: bool):
        if use_old:
            return self.get_old_parameter(key, use_this)

        if use_this:
            return self.get_this_parameter(key)

        if self.local_parameters.parameter_exists(key):
            return self.local_parameters.get_parameter_by_key(key)
        elif self.method_call_parameters.parameter_exists(key):
            return self.method_call_parameters.get_parameter_by_key(key, use_old, use_this)
        elif self.new_instance_variables.parameter_exists(key):
            return self.new_instance_variables.get_parameter_by_key(key)
        elif self.old_instance_variables.parameter_exists(key):
            return self.old_instance_variables.get_parameter_by_key(key)

        raise Exception(f"Parameter {key} does not exist")

    def get_old_parameter(self, key: str, use_this: bool):
        if use_this:
            # Get parameters from the old instance
            if self.old_instance_variables.parameter_exists(key):
                return self.old_instance_variables.get_parameter_by_key(key)

            raise Exception(f"Parameter {key} does not exist in old instance")
        else:
            if self.local_parameters.parameter_exists(key):
                return self.local_parameters.get_parameter_by_key(key)
            if self.method_call_parameters.parameter_exists(key):
                return self.method_call_parameters.get_parameter_by_key(key, use_old=True, use_this=use_this)
            elif self.old_instance_variables.parameter_exists(key):
                return self.old_instance_variables.get_parameter_by_key(key)

            raise Exception(f"Parameter {key} does not exist in old instance or method parameters")

    def get_this_parameter(self, key: str):
        if self.new_instance_variables.parameter_exists(key):
            return self.new_instance_variables.get_parameter_by_key(key)
