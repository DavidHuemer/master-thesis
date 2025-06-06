from definitions.ast.behavior.behaviorNode import BehaviorNode
from definitions.evaluations.tests.testCollections import TestCollections


class BehaviorTest:
    def __init__(self, test_collections: TestCollections, behavior_node: BehaviorNode):
        self.test_collections = test_collections
        self.behavior_type = behavior_node.behavior_type
        self.behavior_node = behavior_node

    def get_test_cases_count(self):
        return self.test_collections.get_test_cases_count()

    def __str__(self):
        return f'"{self.behavior_type.value}" tests: {self.test_collections.get_test_cases_count()}'
