from definitions.ast.astTreeNode import AstTreeNode
from definitions.ast.quantifier.fullRangeTreeNode import FullRangeTreeNode
from definitions.ast.quantifier.numericQuantifierExpressionType import NumericQuantifierExpressionType
from definitions.ast.quantifier.numericQuantifierType import NumericQuantifierType


class NumQuantifierTreeNode(AstTreeNode):
    def __init__(self, name: str, quantifier_type: NumericQuantifierType,
                 quantifier_expression_type: NumericQuantifierExpressionType, expression, variable_names=None,
                 range_: FullRangeTreeNode | None = None):
        super().__init__(name)
        self.quantifier_type = quantifier_type
        self.quantifier_expression_type = quantifier_expression_type
        self.expression = expression
        self.variable_names = variable_names
        self.range_ = range_
