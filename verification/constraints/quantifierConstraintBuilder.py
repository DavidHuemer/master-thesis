from z3 import And

from definitions.ast.quantifier.fullRangeTreeNode import FullRangeTreeNode
from definitions.evaluations.csp.cspParameter import CSPParameter


class QuantifierConstraintBuilder:
    def get_range_expressions(self, range_: FullRangeTreeNode, parameters: dict[str, CSPParameter],
                              constraint_builder):
        expressions = []

        for range_tree_node in range_.ranges:
            parameter = parameters[range_tree_node.name]

            start_expr = constraint_builder.build_expression_constraint(parameters, range_tree_node.start)
            end_expr = constraint_builder.build_expression_constraint(parameters, range_tree_node.end)

            start = self.get_single_range_part(start_expr, range_tree_node.start_operator, parameter.value)
            end = self.get_single_range_part(parameter.value, range_tree_node.end_operator, end_expr)

            and_range = And(start, end)
            expressions.append(and_range)

        return expressions

    @staticmethod
    def get_single_range_part(first, operator: str, second):
        if operator == "<":
            return first < second

        if operator == "<=":
            return first <= second
