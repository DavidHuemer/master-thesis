from definitions.ast import RangeTreeNode
from definitions.ast.astTreeNode import AstTreeNode
from definitions.ast.quantifier.boolQuantifierType import BoolQuantifierType


class BoolQuantifierTreeNode(AstTreeNode):
    def __init__(self, name: str, quantifier_type: BoolQuantifierType, variable_names, ranges: list[RangeTreeNode],
                 expression):
        super().__init__(name)
        self.quantifier_type = quantifier_type
        self.variable_names = variable_names
        self.ranges = ranges
        self.expression = expression

    def get_tree_string(self):
        return f"{self.name} {self.variable_names} {self.ranges} {self.expression}"
