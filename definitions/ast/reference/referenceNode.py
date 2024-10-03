from definitions.ast.astTreeNode import AstTreeNode
from definitions.ast.expressionNode import ExpressionNode
from definitions.ast.reference.referenceType import ReferenceType


class ReferenceNode(AstTreeNode):
    """
    A node representing a reference like \\old or \\this
    """

    def __init__(self, reference_type: ReferenceType, expr: ExpressionNode):
        super().__init__(reference_type.value)
        self.reference_type = reference_type
        self.expr = expr

    def get_tree_string(self):
        return f'{self.name} expr=({self.expr.get_tree_string()})'
