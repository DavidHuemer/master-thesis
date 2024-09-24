from definitions.ast.behavior.behaviorNode import BehaviorNode
from definitions.ast.jmlTreeNode import JmlTreeNode
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

    def get_test_suite(self, test_case: ConsistencyTestCase, method_info: JavaMethod, jml_code: str) -> (
            TestSuite, JmlTreeNode):
        # Steps to build the test suite:
        LoggingHelper.log_info("Building Test Suite")

        # 1. Get the AST of the JML
        ast = self.ast_generator.get_ast(jml_code)

        # TODO: Get test collections for each behavior
        behavior_tests = self.get_behavior_tests(ast, method_info)

        # 2. Get Test Collections
        return TestSuite(test_case, behavior_tests, ast)

    def get_behavior_tests(self, ast: JmlTreeNode, method_info: JavaMethod) -> list[BehaviorTest]:
        return [self.get_behavior_test(behavior_node, method_info) for behavior_node in ast.behavior_nodes]

    def get_behavior_test(self, behavior_node: BehaviorNode, method_info: JavaMethod) -> BehaviorTest:
        test_collections = self.test_collections_builder.build(method_info, behavior_node)
        return BehaviorTest(test_collections, behavior_node)
