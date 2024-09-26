from definitions.ast.behavior.behaviorNode import BehaviorNode
from definitions.ast.jmlTreeNode import JmlTreeNode
from definitions.code.parameterExtractionInfo import ParameterExtractionInfo
from definitions.consistencyTestCase import ConsistencyTestCase
from definitions.evaluations.tests.behaviorTest import BehaviorTest
from definitions.evaluations.tests.testSuite import TestSuite
from definitions.javaMethod import JavaMethod
from helper.logs.loggingHelper import LoggingHelper
from parser.tree.astGenerator import AstGenerator
from verification.testCollections.testCollectionsBuilder import TestCollectionsBuilder


class TestSuiteBuilder:
    def __init__(self, ast_generator=AstGenerator(),
                 test_collections_builder=TestCollectionsBuilder()):
        self.ast_generator = ast_generator
        self.test_collections_builder = test_collections_builder

    def get_test_suite(self, test_case: ConsistencyTestCase, method_info: JavaMethod, jml_code: str) -> TestSuite:
        # Steps to build the test suite:
        LoggingHelper.log_info("Building Test Suite")

        # 1. Get the AST of the JML
        ast = self.ast_generator.get_ast(jml_code)

        behavior_tests = self.get_behavior_tests(ast, method_info.parameters_list)

        # 2. Get Test Collections
        return TestSuite(test_case, behavior_tests, ast)

    def get_behavior_tests(self, ast: JmlTreeNode, parameters: list[ParameterExtractionInfo]) -> list[BehaviorTest]:
        return [self.get_behavior_test(behavior_node, parameters) for behavior_node in ast.behavior_nodes]

    def get_behavior_test(self, behavior_node: BehaviorNode, parameters: list[ParameterExtractionInfo]) -> BehaviorTest:
        test_collections = self.test_collections_builder.build(parameters, behavior_node)
        return BehaviorTest(test_collections, behavior_node)
