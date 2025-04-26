from z3 import Not

from nodes.baseNodeHandler import BaseNodeHandler
from definitions.ast.prefixNode import PrefixNode


class BasePrefixHandler[T](BaseNodeHandler[T]):
    def __init__(self, is_smt: bool):
        super().__init__()
        self.is_smt = is_smt

    def is_node(self, t: T):
        return isinstance(t.node, PrefixNode)

    def handle(self, t: T):
        prefix_expression: PrefixNode = t.node

        expr = self.evaluate_with_runner(t, prefix_expression.expr)

        if prefix_expression.prefix == '++':
            return expr + 1
        elif prefix_expression.prefix == '--':
            return expr - 1
        elif prefix_expression.prefix == '!':
            return Not(expr) if self.is_smt else not expr
        elif prefix_expression.prefix == '+':
            return expr
        elif prefix_expression.prefix == '-':
            return -expr
        elif prefix_expression.prefix == '~':
            return ~expr
