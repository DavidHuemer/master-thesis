from typing import Callable, Any

from z3 import Int, ForAll, And, Implies

from definitions.evaluations.csp.cspParameter import CSPParameter
from definitions.evaluations.csp.jmlProblem import JMLProblem


class ArrayTestConstraintsGenerator:
    """
    Helper class to generate constraints for array parameters that are used in test cases.
    """

    def get_test_constraints(self, jml_problem: JMLProblem, parameter: CSPParameter):
        """
        Returns constraints for the given parameter.
        :param jml_problem: The JML problem
        :param parameter: The array parameter
        :return: A list of constraints
        """

        length_parameter_key = parameter.name + "_length"
        length_parameter = jml_problem.parameters[length_parameter_key]

        yield length_parameter.value == 0

        testing_lengths = [1, 2, 5, 10]
        for length in testing_lengths:
            constraints = self.get_constraints_for_length(parameter, length_parameter, length)
            for constraint in constraints:
                yield constraint

        variable_lengths = [(1, 10), (10, 30)]
        for min_length, max_length in variable_lengths:
            yield And(length_parameter.value >= min_length, length_parameter.value <= max_length)

    def get_constraints_for_length(self, param: CSPParameter, length_param: CSPParameter, length: int):
        if self.is_numeric(param):
            for constraint in self.get_constraints_for_numeric_array(param, length_param, length):
                yield constraint
        else:
            return []

    def get_constraints_for_numeric_array(self, param: CSPParameter, length_param: CSPParameter, length: int):
        index = Int('index')
        for i in [-1, 0, 1]:
            yield self.get_for_all(index, length_param, length, param.value[index] == i)

        # distinct constraint:
        distinct_constraint = [param.value[i] != param.value[i + 1] for i in range(length - 1)]
        and_distinct = And(*distinct_constraint)
        yield And(and_distinct, length_param.value == length)

        # Alternating < and >
        yield self.get_by_indexes_and(
            lambda i: param.value[i] < param.value[i + 1] if i % 2 == 0 else param.value[i] > param.value[i + 1],
            length_param, length
        )

        # From smallest to largest
        yield self.get_by_indexes_and(lambda i: param.value[i] < param.value[i + 1], length_param, length)

    @staticmethod
    def get_for_all(index: Int, length_param: CSPParameter, length: int, constraint):
        return And(ForAll(index, Implies(And(index >= 0, index < length), constraint)),
                   length_param.value == length)

    @staticmethod
    def get_by_indexes_and(get_constraint: Callable[[int], Any], length_param: CSPParameter, length: int):
        constraints = [get_constraint(i) for i in range(length)]
        return And(And(*constraints), length_param.value == length)

    @staticmethod
    def is_numeric(parameter: CSPParameter):
        # parameter type is e.g. int[]. So we need to remove the []
        param_type = parameter.param_type[:-2]
        return param_type in ["int", "long", "float", "double"]
