from definitions.ast.expressionNode import ExpressionNode
from definitions.code.parameterExtractionInfo import ParameterExtractionInfo
from definitions.evaluations.tests.testCollection import TestCollection
from verification.jmlProblem.jmlProblemBuilder import JMLProblemBuilder
from verification.testCase.testCaseGenerator import TestCasesGenerator


class TestCollectionBuilder:
    """
    Helper class for building a single TestCollection
    """

    def __init__(self, jml_problem_builder=JMLProblemBuilder(), test_cases_generator=TestCasesGenerator()):
        self.jml_problem_builder = jml_problem_builder
        self.test_cases_generator = test_cases_generator

    def build(self, parameters: list[ParameterExtractionInfo], expressions: list[ExpressionNode]) -> TestCollection:
        """
        Builds a single test collection out of expressions
        :param parameters: The parameters of the method
        :param expressions: The list of expressions that are used to generate the test cases
        :return: The test collection
        """
        # First get the JMLProblem
        jml_problem = self.jml_problem_builder.build(parameters, expressions)

        # Then generate the test cases out of the JMLProblem
        test_cases = self.test_cases_generator.generate(jml_problem)

        return TestCollection(test_cases, jml_problem.parameters.csp_parameters)
