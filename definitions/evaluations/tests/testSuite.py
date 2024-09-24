from definitions.ast.jmlTreeNode import JmlTreeNode
from definitions.consistencyTestCase import ConsistencyTestCase
from definitions.evaluations.tests.behaviorTest import BehaviorTest


class TestSuite:
    def __init__(self, consistency_test_case: ConsistencyTestCase, behavior_tests: list[BehaviorTest],
                 ast: JmlTreeNode):
        self.consistency_test_case = consistency_test_case
        self.behavior_tests = behavior_tests
        self.ast = ast

    def get_java(self):
        return self.consistency_test_case.java_code
