from definitions.ast.astTreeNode import AstTreeNode
from definitions.ast.expressionNode import ExpressionNode


class ArrayIndexNode(AstTreeNode):
    def __init__(self, arr_expression: ExpressionNode, index_expression: ExpressionNode):
        super().__init__("ArrayIndex")
        self.arr_expression = arr_expression
        self.index_expression = index_expression

    def get_tree_string(self):
        return f"{self.name} [{self.index_expression}]"
