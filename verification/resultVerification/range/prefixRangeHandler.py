from z3 import Not

from definitions.ast.prefixNode import PrefixNode
from nodes.baseNodeHandler import BaseNodeHandler
from verification.resultVerification.range.rangeDto import RangeDto


class PrefixRangeHandler(BaseNodeHandler[RangeDto]):

    def is_node(self, t: RangeDto):
        return isinstance(t.node, PrefixNode)

    def handle(self, t: RangeDto):
        prefix_expression: PrefixNode = t.node

        expr = self.get_expr(prefix_expression, t)

        if prefix_expression.prefix == '++':
            return expr + 1
        elif prefix_expression.prefix == '--':
            return expr - 1
        elif prefix_expression.prefix == '!':
            return Not(expr)
        elif prefix_expression.prefix == '+':
            return expr
        elif prefix_expression.prefix == '-':
            return -expr
        elif prefix_expression.prefix == '~':
            return ~expr

    @staticmethod
    def get_expr(prefix_expression: PrefixNode, t: RangeDto):
        return t.constraint_builder.evaluate(t.copy_with_other_node(prefix_expression.expr))
