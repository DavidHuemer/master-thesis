from definitions.ast.expressionNode import ExpressionNode
from definitions.code.parameterExtractionInfo import ParameterExtractionInfo
from definitions.evaluations.tests.testCollection import TestCollection
from definitions.parameters.Variables import Variables
from testGeneration.testCaseGeneration.testCaseGenerator import generate_test_cases
from testGeneration.testCollections.jmlProblemBuilder import build_jml_problem


def build_test_collection(parameters: Variables, expressions: list[ExpressionNode]):
    """
    Builds a single test collection out of expressions
    :param parameters: The parameters of the method
    :param expressions: The list of expressions that are used to generate the test cases
    :return: The test collection
    """
    # First get the JMLProblem
    jml_problem = build_jml_problem(parameters, expressions)

    # Then generate the test cases out of the JMLProblem

    return TestCollection(test_cases=generate_test_cases(jml_problem))
