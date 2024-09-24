from definitions.ast.behavior.behaviorNode import BehaviorNode
from definitions.evaluations.tests.testCollections import TestCollections


class BehaviorTest:
    def __init__(self, test_collections: TestCollections, behavior_node: BehaviorNode):
        self.test_collections = test_collections
        self.behavior_type = behavior_node.behavior_type
        self.behavior_node = behavior_node
