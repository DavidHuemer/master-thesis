from definitions.ast.arrayIndexNode import ArrayIndexNode
from nodes.baseNodeHandler import BaseNodeHandler


class BaseArrayIndexNodeHandler[T](BaseNodeHandler[T]):
    def is_node(self, t: T):
        return isinstance(t.node, ArrayIndexNode)

    def handle(self, t: T):
        expression: ArrayIndexNode = t.node
        array_expr = self.evaluate_with_runner(t, expression.arr_expression)
        index_expr = self.evaluate_with_runner(t, expression.index_expression)
        return array_expr[index_expr]
