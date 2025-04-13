from typing import Callable, Any

from z3 import ArrayRef, Sum, Product, If, And

from definitions.ast.quantifier.numQuantifierTreeNode import NumQuantifierTreeNode
from definitions.ast.quantifier.numericQuantifierType import NumericQuantifierType
from definitions.evaluations.csp.parameters.cspParamHelperType import CSPParamHelperType
from nodes.baseNodeHandler import BaseNodeHandler
from testGeneration.constraints.constraintArrayValueHelper import ConstraintArrayValueHelper
from testGeneration.constraints.constraintsDto import ConstraintsDto


class NumQuantifierValueConstraintBuilder(BaseNodeHandler[ConstraintsDto]):
    def __init__(self, array_value_helper=ConstraintArrayValueHelper()):
        super().__init__()
        self.array_value_helper = array_value_helper

    def evaluate(self, expression, t: ConstraintsDto):
        values: list = self.get_values(expression, t)
        if len(values) == 0:
            return None

        if expression.quantifier_type == NumericQuantifierType.MAX:
            return self.get_max(values, values)

        if expression.quantifier_type == NumericQuantifierType.MIN:
            return self.get_min(values, values)

        if expression.quantifier_type == NumericQuantifierType.SUM:
            return Sum(*values)

        if expression.quantifier_type == NumericQuantifierType.PRODUCT:
            return Product(*values)

        raise Exception("Numeric quantifier expression type not supported")

    def get_max(self, all_values: list, remaining_values: list):
        value = remaining_values[0]

        if len(remaining_values) == 1:
            return value

        max_and = self.get_comparison(value, all_values, lambda a, b: a >= b)
        return If(max_and, value, self.get_max(all_values, remaining_values[1:]))

    def get_min(self, all_values: list, remaining_values: list):
        value = remaining_values[0]

        if len(remaining_values) == 1:
            return value

        min_and = self.get_comparison(value, all_values, lambda a, b: a <= b)
        return If(min_and, value, self.get_min(all_values, remaining_values[1:]))

    @staticmethod
    def get_comparison(value, values: list, comparison: Callable[[Any, Any], Any]):
        comparisons = [comparison(value, val) for val in values]
        return And(*comparisons)

    def get_values(self, expression: NumQuantifierTreeNode, t: ConstraintsDto):
        expression_list = [self.evaluate_with_runner(t, expr) for
                           expr in expression.expressions]

        values = []

        for expr in expression_list:
            if isinstance(expr, ArrayRef):
                length_param = t.constraint_parameters.csp_parameters[str(expr)].length_param
                value = self.array_value_helper.get_value_from_array(expr,
                                                                     length_param,
                                                                     expression.quantifier_type,
                                                                     t)
                values.append(value)
            else:
                values.append(expr)

        return values
