from definitions.ast.prefixNode import PrefixNode
from definitions.evaluations.BaseDto import BaseDto
from nodes.baseNodeHandler import BaseNodeHandler


class BasePrefixConstraintBuilder(BaseNodeHandler[BaseDto]):
    def is_node(self, t: BaseDto):
        return isinstance(t.node, PrefixNode)

    def handle(self, t: BaseDto):
        prefix_expression: PrefixNode = t.node

        expr = t.evaluate_with_other_node(prefix_expression.prefix)

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
