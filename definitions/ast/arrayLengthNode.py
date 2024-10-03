from definitions.ast.astTreeNode import AstTreeNode
from definitions.ast.expressionNode import ExpressionNode


class ArrayLengthNode(AstTreeNode):
    def __init__(self, arr_expr: ExpressionNode):
        super().__init__("Array Length")
        self.arr_expr = arr_expr
        self.children = [arr_expr]
