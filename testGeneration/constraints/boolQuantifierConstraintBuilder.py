from z3 import And, ForAll, Implies, Exists

from definitions.ast.quantifier.boolQuantifierTreeNode import BoolQuantifierTreeNode
from definitions.ast.quantifier.boolQuantifierType import BoolQuantifierType
from nodes.baseNodeHandler import BaseNodeHandler
from testGeneration.constraints.constraintsDto import ConstraintsDto
from testGeneration.constraints.quantifier.quantifierRangeValuesHelper import QuantifierRangeValuesHelper


class BoolQuantifierConstraintBuilder(BaseNodeHandler[ConstraintsDto]):
    def __init__(self, quantifier_range_values_helper=None):
        super().__init__()
        self.quantifier_range_values_helper = quantifier_range_values_helper or QuantifierRangeValuesHelper()

    def is_node(self, t: ConstraintsDto):
        return isinstance(t.node, BoolQuantifierTreeNode)

    def handle(self, t: ConstraintsDto):
        expression: BoolQuantifierTreeNode = t.node
        variables = self.quantifier_range_values_helper.get_variables(expression)

        for var in variables:
            t.constraint_parameters.loop_parameters.add_csp_parameter(var)

        range_expressions = self.evaluate_with_runner(t, expression.range_)
        final_expr = self.evaluate_with_runner(t, expression.expression)

        variable_values = [var.value for var in variables]

        if expression.quantifier_type == BoolQuantifierType.FORALL:
            return ForAll(*variable_values, Implies(range_expressions, final_expr))
        elif expression.quantifier_type == BoolQuantifierType.EXISTS:
            return Exists(*variable_values, And(range_expressions, final_expr))

    @staticmethod
    def evaluate_for_all(variable_values, range_, expr):
        return ForAll(*variable_values, Implies(range_, expr))

    @staticmethod
    def evaluate_exists(variable_values, range_, expr):
        return Exists(*variable_values, And(range_, expr))
