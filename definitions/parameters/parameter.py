from copy import copy

from z3 import ModelRef, And

from definitions.parameters.parameterState import ParameterState
from definitions.parameters.parameterValue import ParameterValue
from testGeneration.modelValueExtractor import get_parameter_value
from verification.csp.cspParamBuilder import build_csp_param


class Parameter:
    """
    This class represents a parameter
    It contains the CSP parameter as well as the real values
    """

    def __init__(self, old: ParameterState, new: ParameterState | None):
        self.name = old.csp_parameter.name
        self.java_type = old.csp_parameter.param_type
        # self.java_type = java_type
        # self._dimension = dimension
        # self.csp_parameter = build_csp_param(java_type, name, dimension)

        self.old = old
        self.new: ParameterState | None = new

    def evaluate(self, model: ModelRef, func_decl_dict, use_old: bool = False):
        state = self.get_state(use_old)
        csp_param = state.csp_parameter
        state.parameter_value = get_parameter_value(csp_param, model, func_decl_dict)

    def get_constraint(self, use_old: bool = False):
        """
        Returns the constraint of the parameter
        :return: The constraint of the parameter
        """
        state = self.get_state(use_old)
        if state.parameter_value is None:
            raise Exception("Parameter value is None - cannot get constraint")

        if state.parameter_value.python_value is None:
            return state.csp_parameter.is_null_param == True

        if self.is_array():
            length_equal_constraint = state.csp_parameter.length_param == len(state.parameter_value.python_value)
            index_constraints = [state.csp_parameter.value[i] == state.parameter_value.python_value[i] for i in
                                 range(len(state.parameter_value.python_value))]

            return And(length_equal_constraint, *index_constraints)

        return state.csp_parameter.value == state.parameter_value.python_value

    def get_state(self, use_old: bool = False) -> ParameterState:
        """
        Returns a parameter state
        If the new state is not None, it returns the new state except use_old is set to True
        If the new state is None, it returns the old state
        :param use_old: if True, the old state is returned
        :return: the parameter state
        """

        if self.new is not None and not use_old:
            return self.new
        elif self.old is not None:
            return self.old
        else:
            raise Exception("No parameter state available")

    def update_new(self, parameter_value: ParameterValue):
        """
        Updates the new parameter value
        :param parameter_value: The new parameter value
        :return: None
        """
        new_param_csp = build_csp_param(self.java_type, self.name, 1 if self.is_array() else 0)
        new_parameter_state = ParameterState(new_param_csp)
        new_parameter_state.parameter_value = parameter_value
        self.new = new_parameter_state

    def is_array(self):
        return self.old.csp_parameter.is_array()

    def __copy__(self):
        return Parameter(copy(self.old), copy(self.new))

    def __str__(self):
        return f"{self.java_type} {self.name}{'[]' if self.is_array() else ''}"
