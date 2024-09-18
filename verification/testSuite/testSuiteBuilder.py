from definitions.ast.jmlTreeNode import JmlTreeNode
from definitions.evaluations.tests.testSuite import TestSuite
from definitions.inconsistencyTestCase import InconsistencyTestCase
from definitions.javaMethod import JavaMethod
from parser.tree.astGenerator import AstGenerator
from verification.testCollections.testCollectionsBuilder import TestCollectionsBuilder


class TestSuiteBuilder:
    def __init__(self, ast_generator=AstGenerator(),
                 test_collections_builder=TestCollectionsBuilder()):
        self.ast_generator = ast_generator
        self.test_collections_builder = test_collections_builder

    def get_test_suite(self, test_case: InconsistencyTestCase, method_info: JavaMethod, jml_code: str) -> (
            TestSuite, JmlTreeNode):
        # Steps to build the test suite:

        # 1. Get the AST of the JML
        ast = self.ast_generator.get_ast(jml_code)

        # 2. Get Test Collections
        test_collections = self.test_collections_builder.build(method_info, ast)
        return TestSuite(test_case, test_collections, ast)
