from z3 import And, If, Sum, Product

from definitions.ast.quantifier.numQuantifierTreeNode import NumQuantifierTreeNode
from definitions.ast.quantifier.numericQuantifierExpressionType import NumericQuantifierExpressionType
from definitions.evaluations.csp.cspParameter import CSPParameter
from definitions.ast.quantifier.numericQuantifierType import NumericQuantifierType


class NumQuantifierConstraintBuilder:
    def evaluate(self, parameters: dict[str, CSPParameter], expression: NumQuantifierTreeNode,
                 expression_constraint_builder):
        if expression.quantifier_expression_type == NumericQuantifierExpressionType.VALUE:
            return self.evaluate_with_value(expression, parameters, expression_constraint_builder)
        elif expression.quantifier_expression_type == NumericQuantifierExpressionType.RANGE:
            return self.evaluate_with_range()

        raise Exception("NumQuantifierConstraintBuilder: Invalid quantifier expression type")

    def evaluate_with_value(self, expression: NumQuantifierTreeNode, parameters: dict[str, CSPParameter],
                            expression_constraint_builder):
        values = [expression_constraint_builder.build_expression_constraint(parameters, expr) for expr in
                  expression.expressions]
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
