from z3 import Not

from definitions.ast.prefixNode import PrefixNode
from definitions.evaluations.BaseDto import BaseDto
from nodes.baseNodeHandler import BaseNodeHandler


class BasePrefixConstraintBuilder(BaseNodeHandler[BaseDto]):
    def is_node(self, t: BaseDto):
        return isinstance(t.node, PrefixNode)

    def handle(self, t: BaseDto):
        prefix_expression: PrefixNode = t.node

        expr = self.evaluate_with_runner(t, prefix_expression.expr)

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
