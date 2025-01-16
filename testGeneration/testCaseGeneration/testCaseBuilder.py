from z3 import ModelRef, ArrayRef, BoolRef, SeqRef, QuantifierRef

from definitions.evaluations.csp.jmlProblem import JMLProblem
from definitions.evaluations.csp.parameters.cspParamHelperType import CSPParamHelperType
from definitions.evaluations.csp.parameters.methodCallParameters import MethodCallParameters
from definitions.verification.testCase import TestCase


def build_test_case(jml_problem: JMLProblem, solution: ModelRef) -> TestCase:
    """
    Builds a test case from a solution
    :param jml_problem: The JML problem
    :param solution: The solution to build the test case from
    :return: The test case
    """

    method_call_parameters = MethodCallParameters()
    solution_param_keys = [str(var) for var in solution]
    required_param_keys = [param.name for param in jml_problem.parameters.csp_parameters.get_actual_parameters()]

    for parameter_key in required_param_keys:
        if parameter_key not in solution_param_keys:
            method_call_parameters[parameter_key] = None
            break

        jml_problem_param = jml_problem.parameters.csp_parameters[parameter_key]
        solution_param = solution[jml_problem_param.value]
        null_value_key = f"{parameter_key}_is_null"
        # TODO: Add support for char, string
        if null_value_key in solution_param_keys and solution[
            jml_problem.parameters.csp_parameters[null_value_key].value]:
            method_call_parameters[parameter_key] = None
        elif hasattr(solution_param, "as_long"):
            method_call_parameters[parameter_key] = solution_param.as_long()
        elif isinstance(solution_param, ArrayRef) or isinstance(solution_param, QuantifierRef):
            array_values = get_array_values(jml_problem, jml_problem_param, parameter_key, solution)
            method_call_parameters[parameter_key] = array_values
        elif isinstance(solution_param, BoolRef):
            method_call_parameters[parameter_key] = str(solution_param).lower() == 'true'
        elif isinstance(solution_param, SeqRef):
            method_call_parameters[parameter_key] = str(solution_param)
        else:
            raise Exception(f"Unsupported parameter type: {type(solution_param)}")

    return TestCase(method_call_parameters)


def get_array_values(jml_problem: JMLProblem, jml_problem_param, parameter_key: str, solution: ModelRef):
    # Get array length
    length_param = jml_problem.parameters.csp_parameters.get_helper(parameter_key, CSPParamHelperType.LENGTH)
    length_value = solution[length_param.value].as_long()
    # Get array values
    array_values = []
    for i in range(length_value):
        value = solution.evaluate(jml_problem_param.value[i]).as_long()
        array_values.append(value)
    return array_values
