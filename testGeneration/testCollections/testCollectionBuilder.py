import sys

from definitions.ast.expressionNode import ExpressionNode
from definitions.code.parameterExtractionInfo import ParameterExtractionInfo
from definitions.evaluations.tests.testCollection import TestCollection
from testGeneration.testCollections.jmlProblemBuilder import build_jml_problem
from testGeneration.testCaseGeneration.testCaseGenerator import generate_test_cases


def build_test_collection(parameters: list[ParameterExtractionInfo], expressions: list[ExpressionNode]):
    """
    Builds a single test collection out of expressions
    :param parameters: The parameters of the method
    :param expressions: The list of expressions that are used to generate the test cases
    :return: The test collection
    """
    # First get the JMLProblem
    jml_problem = build_jml_problem(parameters, expressions)

    jml_problem_size = sys.getsizeof(jml_problem)

    # Then generate the test cases out of the JMLProblem

    return TestCollection(test_cases=generate_test_cases(jml_problem),
                          csp_parameters=jml_problem.parameters.csp_parameters)
