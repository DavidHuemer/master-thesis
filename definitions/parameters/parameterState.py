from definitions.evaluations.csp.cspParameter import CSPParameter
from definitions.parameters.parameterValue import ParameterValue


class ParameterState:
    """
    Represents the state (before and after the execution of a method) of a parameter.
    """

    def __init__(self, csp_parameter: CSPParameter):
        self.csp_parameter = csp_parameter
        self.parameter_value: ParameterValue | None = None

    def __copy__(self):
        """
        Returns a copy of the parameter state.
        :return: A copy of the parameter state.
        """
        return ParameterState(self.csp_parameter)
