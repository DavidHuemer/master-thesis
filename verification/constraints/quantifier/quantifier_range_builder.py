from z3 import And

from definitions.ast.quantifier.fullRangeTreeNode import FullRangeTreeNode
from verification.constraints.constraintsDto import ConstraintsDto


class QuantifierRangeBuilder:
    def get_range_expressions(self, range_: FullRangeTreeNode, t: ConstraintsDto):
        expressions = []

        for range_tree_node in range_.ranges:
            parameter = t.constraint_parameters.get_parameter_by_key(range_tree_node.name)

            start_expr = t.constraint_builder.evaluate(t.copy_with_other_node(range_tree_node.start))
            end_expr = t.constraint_builder.evaluate(t.copy_with_other_node(range_tree_node.end))

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
