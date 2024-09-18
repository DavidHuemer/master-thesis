from definitions.ast.jmlTreeNode import JmlTreeNode
from definitions.evaluations.tests.testCollections import TestCollections
from definitions.inconsistencyTestCase import InconsistencyTestCase


class TestSuite:
    def __init__(self, inconsistency_test_case: InconsistencyTestCase, test_collections: TestCollections,
                 ast: JmlTreeNode):
        self.inconsistency_test_case = inconsistency_test_case
        self.test_collections = test_collections
        self.ast = ast

    def get_java(self):
        return self.inconsistency_test_case.java_code
