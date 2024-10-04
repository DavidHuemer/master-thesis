from definitions.ast.quantifier.fullRangeTreeNode import FullRangeTreeNode
from definitions.ast.quantifier.numericQuantifierExpressionType import NumericQuantifierExpressionType
from definitions.ast.quantifier.numericQuantifierType import NumericQuantifierType
from definitions.ast.quantifier.quantifierTreeNode import QuantifierTreeNode


class NumQuantifierTreeNode(QuantifierTreeNode):
    def __init__(self, name: str, quantifier_type: NumericQuantifierType,
                 quantifier_expression_type: NumericQuantifierExpressionType, expressions,
                 variable_names: list[tuple[str, str]] | None = None,
                 range_: FullRangeTreeNode | None = None):
        super().__init__(name, variable_names, range_)
        self.quantifier_type = quantifier_type
        self.quantifier_expression_type = quantifier_expression_type
        self.expressions = expressions
