from definitions.ast.astTreeNode import AstTreeNode
from definitions.ast.expressionNode import ExpressionNode


class ArrayIndexNode(AstTreeNode):
    def __init__(self, name: str, expression: ExpressionNode):
        super().__init__(name)
        self.expression = expression

    def get_tree_string(self):
        return f"{self.name} [{self.expression}]"
