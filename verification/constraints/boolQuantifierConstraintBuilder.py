from z3 import And, ForAll, Implies, Exists

from definitions.ast.quantifier.boolQuantifierTreeNode import BoolQuantifierTreeNode
from definitions.ast.quantifier.boolQuantifierType import BoolQuantifierType
from nodes.baseNodeHandler import BaseNodeHandler
from verification.constraints.constraintsDto import ConstraintsDto
from verification.constraints.quantifier.quantifierRangeValuesHelper import QuantifierRangeValuesHelper


class BoolQuantifierConstraintBuilder(BaseNodeHandler[ConstraintsDto]):
    def __init__(self, quantifier_range_values_helper=QuantifierRangeValuesHelper()):
        self.quantifier_range_values_helper = quantifier_range_values_helper

    def is_node(self, t: ConstraintsDto):
        return isinstance(t.node, BoolQuantifierTreeNode)

    def handle(self, t: ConstraintsDto):
        expression: BoolQuantifierTreeNode = t.node
        variables = self.quantifier_range_values_helper.get_variables(expression)

        for var in variables:
            # TODO: Check if variable already exists
            t.constraint_parameters.loop_parameters.add_csp_parameter(var)

        range_expressions = t.constraint_builder.evaluate(t.copy_with_other_node(expression.range_))
        final_expr = t.constraint_builder.evaluate(t.copy_with_other_node(expression.expression))

        variable_values = [var.value for var in variables]

        if expression.quantifier_type == BoolQuantifierType.FORALL:
            return self.evaluate_for_all(variable_values, range_expressions, final_expr)
        elif expression.quantifier_type == BoolQuantifierType.EXISTS:
            return self.evaluate_exists(variable_values, range_expressions, final_expr)

    @staticmethod
    def evaluate_for_all(variable_values, range_, expr):
        return ForAll(*variable_values, Implies(range_, expr))

    @staticmethod
    def evaluate_exists(variable_values, range_, expr):
        return Exists(*variable_values, And(range_, expr))
