from definitions.ast import RangeTreeNode
from definitions.ast.astTreeNode import AstTreeNode


class BoolQuantifierTreeNode(AstTreeNode):
    def __init__(self, name: str, variable_names, ranges: list[RangeTreeNode], expression):
        super().__init__(name)
        self.variable_names = variable_names
        self.ranges = ranges
        self.expression = expression

    def get_tree_string(self):
        return f"{self.name} {self.variable_names} {self.ranges} {self.expression}"
