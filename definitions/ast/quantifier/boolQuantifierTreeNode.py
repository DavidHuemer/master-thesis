from definitions.ast.astTreeNode import AstTreeNode
from definitions.ast.quantifier.boolQuantifierType import BoolQuantifierType
from definitions.ast.quantifier.quantifierTreeNode import QuantifierTreeNode


class BoolQuantifierTreeNode(QuantifierTreeNode):
    def __init__(self, name: str, quantifier_type: BoolQuantifierType, variable_names: list[tuple[str, str]] | None,
                 range_: AstTreeNode,
                 expression):
        super().__init__(name, variable_names, range_)
        self.quantifier_type = quantifier_type
        self.expression = expression

    def get_tree_string(self):
        return f"{self.name} {self.variable_names} {self.range_} {self.expression}"
