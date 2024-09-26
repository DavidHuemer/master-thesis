from z3 import Int, ForAll, And

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

        testing_lengths = [1, 2, 3, 5, 10]
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

    @staticmethod
    def get_constraints_for_numeric_array(param: CSPParameter, length_param: CSPParameter, length: int):
        index = Int('index')
        # # Every parameter is 0
        yield And(ForAll(index, param.value[index] == 0), length_param.value == length)
        # Every parameter is 1
        index = Int('index')
        yield And(ForAll(index, param.value[index] == 1), length_param.value == length)

        index = Int('index')
        distinct_constraint = [param.value[i] != param.value[i + 1] for i in range(length - 1)]
        and_distinct = And(*distinct_constraint)
        yield And(and_distinct, length_param.value == length, ForAll(index, param.value[index] > 10))

        # Alternating < and >
        index = Int('index')
        alternating_constraint = [
            param.value[i] < param.value[i + 1] if i % 2 == 0 else param.value[i] > param.value[i + 1] for i in
            range(length - 1)]

        and_alternating = And(*alternating_constraint)
        yield And(and_alternating, length_param.value == length, ForAll(index, param.value[index] > 0))

        # From smallest to largest
        index = Int('index')
        increasing_constraint = [param.value[i] < param.value[i + 1] for i in range(length - 1)]
        and_increasing = And(*increasing_constraint)
        yield And(and_increasing, length_param.value == length, ForAll(index, param.value[index] > 0))

    @staticmethod
    def is_numeric(parameter: CSPParameter):
        # parameter type is e.g. int[]. So we need to remove the []
        param_type = parameter.param_type[:-2]
        return param_type in ["int", "long", "float", "double"]
