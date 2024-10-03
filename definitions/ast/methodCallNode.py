from definitions.ast.astTreeNode import AstTreeNode
from definitions.ast.expressionNode import ExpressionNode


class MethodCallNode(AstTreeNode):
    """
    A node representing a method call
    """

    def __init__(self, ident: str, args=list[ExpressionNode]):
        super().__init__(ident)
        self.args = args

        self.children = args

    def get_tree_string(self):
        return f'{self.name} args=({self.args})'
