from definitions.ast.quantifier.numQuantifierTreeNode import NumQuantifierTreeNode
from definitions.ast.quantifier.numericQuantifierExpressionType import NumericQuantifierExpressionType
from nodes.baseNodeHandler import BaseNodeHandler
from testGeneration.constraints.constraintArrayValueHelper import ConstraintArrayValueHelper
from testGeneration.constraints.constraintsDto import ConstraintsDto
from testGeneration.constraints.quantifier.numQuantifierRangeConstraintBuilder import \
    NumQuantifierRangeConstraintBuilder
from testGeneration.constraints.quantifier.numQuantifierValueConstraintBuilder import \
    NumQuantifierValueConstraintBuilder


class NumQuantifierConstraintBuilder(BaseNodeHandler[ConstraintsDto]):
    def __init__(self, array_value_helper=ConstraintArrayValueHelper(),
                 num_quantifier_range_constraint_builder=NumQuantifierRangeConstraintBuilder(),
                 num_quantifier_value_constraint_builder=NumQuantifierValueConstraintBuilder()):
        super().__init__()
        self.array_value_helper = array_value_helper
        self.num_quantifier_range_constraint_builder = num_quantifier_range_constraint_builder
        self.num_quantifier_value_constraint_builder = num_quantifier_value_constraint_builder

    def is_node(self, t: ConstraintsDto):
        return isinstance(t.node, NumQuantifierTreeNode)

    def handle(self, t: ConstraintsDto):
        expression: NumQuantifierTreeNode = t.node
        if expression.quantifier_expression_type == NumericQuantifierExpressionType.VALUE:
            return self.num_quantifier_value_constraint_builder.evaluate(expression, t)
        elif expression.quantifier_expression_type == NumericQuantifierExpressionType.RANGE:
            return self.num_quantifier_range_constraint_builder.evaluate(expression, t)

        raise Exception("NumQuantifierConstraintBuilder: Invalid quantifier expression type")

    def set_runner(self, runner):
        super().set_runner(runner)
        self.num_quantifier_range_constraint_builder.set_runner(runner)
        self.num_quantifier_value_constraint_builder.set_runner(runner)


