from definitions.ast.astTreeNode import AstTreeNode
from definitions.ast.expressionNode import ExpressionNode


class PrefixNode(AstTreeNode):
    def __init__(self, prefix: str, expr: ExpressionNode):
        super().__init__("Prefix")
        self.prefix = prefix
        self.expr = expr

    def get_tree_string(self):
        return f"{self.prefix} {self.expr.get_tree_string()}"
