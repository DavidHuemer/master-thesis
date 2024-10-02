from z3 import And, If, Sum, Product, ArrayRef

from definitions.ast.quantifier.numQuantifierTreeNode import NumQuantifierTreeNode
from definitions.ast.quantifier.numericQuantifierExpressionType import NumericQuantifierExpressionType
from definitions.ast.quantifier.numericQuantifierType import NumericQuantifierType
from definitions.evaluations.csp.cspParameter import CSPParameter
from verification.constraints.constraintArrayValueHelper import ConstraintArrayValueHelper


class NumQuantifierConstraintBuilder:
    def __init__(self, array_value_helper=ConstraintArrayValueHelper()):
        self.array_value_helper = array_value_helper

    def evaluate(self, parameters: dict[str, CSPParameter], expression: NumQuantifierTreeNode,
                 expression_constraint_builder):
        if expression.quantifier_expression_type == NumericQuantifierExpressionType.VALUE:
            return self.evaluate_with_value(expression, parameters, expression_constraint_builder)
        elif expression.quantifier_expression_type == NumericQuantifierExpressionType.RANGE:
            return self.evaluate_with_range()

        raise Exception("NumQuantifierConstraintBuilder: Invalid quantifier expression type")

    def evaluate_with_value(self, expression: NumQuantifierTreeNode, parameters: dict[str, CSPParameter],
                            expression_constraint_builder):
        values = self.get_values(expression, parameters, expression_constraint_builder)
        return self.evaluate_list(expression, values)

    def evaluate_with_range(self):
        # TODO: Evaluate with range
        pass

    def evaluate_list(self, expression: NumQuantifierTreeNode, values: list):
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

        max_and = self.get_max_and(value, all_values)
        return If(max_and, value, self.get_max(all_values, remaining_values[1:]))

    def get_min(self, all_values: list, remaining_values: list):
        value = remaining_values[0]

        if len(remaining_values) == 1:
            return value

        min_and = self.get_min_and(value, all_values)
        return If(min_and, value, self.get_min(all_values, remaining_values[1:]))

    def get_max_and(self, value, values: list):
        comparisons = [value >= val for val in values]
        return And(*comparisons)

    def get_min_and(self, value, values: list):
        comparisons = [value <= val for val in values]
        return And(*comparisons)

    def get_values(self, expression: NumQuantifierTreeNode, parameters: dict[str, CSPParameter],
                   expression_constraint_builder):
        expression_list = [expression_constraint_builder.build_expression_constraint(parameters, expr) for expr in
                           expression.expressions]

        values = []

        for expr in expression_list:
            if isinstance(expr, ArrayRef):
                length_param = parameters[f"{str(expr)}_length"]
                value = self.array_value_helper.get_value_from_array(expr, length_param, expression.quantifier_type)
                values.append(value)
            else:
                values.append(expr)

        return values
