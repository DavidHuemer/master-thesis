from definitions.ast.astTreeNode import AstTreeNode
from definitions.ast.behavior.behaviorNode import BehaviorNode


class JmlTreeNode(AstTreeNode):
    def __init__(self, behavior_nodes: list[BehaviorNode]):
        super().__init__("JML")
        self.behavior_nodes = behavior_nodes

        self.children = behavior_nodes

    def get_tree_string(self):
        return f"{self.name} ({[x.get_tree_string() for x in self.behavior_nodes]})"

    def __str__(self):
        return self.get_tree_string()
