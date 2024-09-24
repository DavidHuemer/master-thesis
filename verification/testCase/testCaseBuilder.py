from z3 import ModelRef, ArrayRef, Select, QuantifierRef

from definitions.evaluations.csp.jmlProblem import JMLProblem
from definitions.verification.testCase import TestCase


class TestCaseBuilder:
    def build_test_case(self, jml_problem: JMLProblem, solution: ModelRef) -> TestCase:
        """
        Builds a test case from a solution
        :param jml_problem: The JML problem
        :param solution: The solution to build the test case from
        :return: The test case
        """

        parameters_dict = dict()
        solution_param_keys = [str(var) for var in solution]
        required_param_keys = [param for param in jml_problem.parameters if not jml_problem.parameters[param].is_helper]

        for parameter_key in required_param_keys:
            if parameter_key in solution_param_keys:
                jml_problem_param = jml_problem.parameters[parameter_key]
                solution_param = solution[jml_problem_param.value]
                null_value_key = f"{parameter_key}_is_null"
                if null_value_key in solution_param_keys and solution[jml_problem.parameters[null_value_key].value]:
                    parameters_dict[parameter_key] = None
                elif hasattr(solution_param, "as_long"):
                    parameters_dict[parameter_key] = solution_param.as_long()
                elif isinstance(solution_param, ArrayRef) or isinstance(solution_param, QuantifierRef):
                    array_values = self.get_array_values(jml_problem, jml_problem_param, parameter_key, solution)
                    parameters_dict[parameter_key] = array_values
                else:
                    raise Exception(f"Unsupported parameter type: {type(solution_param)}")
            else:
                parameters_dict[parameter_key] = None  # TODO: Generate random value

        return TestCase(parameters_dict)

    @staticmethod
    def get_array_values(jml_problem: JMLProblem, jml_problem_param, parameter_key: str, solution: ModelRef):
        # Get array length
        length_name = f"{parameter_key}_length"
        length_value = solution[jml_problem.parameters[length_name].value].as_long()
        # Get array values
        array_values = []
        for i in range(length_value):
            value = solution.evaluate(jml_problem_param.value[i]).as_long()
            array_values.append(value)
        return array_values
