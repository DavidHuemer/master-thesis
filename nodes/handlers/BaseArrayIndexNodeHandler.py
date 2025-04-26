from z3 import ArithRef

from definitions.ast.arrayIndexNode import ArrayIndexNode
from helper.z3Helper import get_z3_value
from nodes.baseNodeHandler import BaseNodeHandler


class BaseArrayIndexNodeHandler[T](BaseNodeHandler[T]):
    def is_node(self, t: T):
        return isinstance(t.node, ArrayIndexNode)

    def handle(self, t: T):
        expression: ArrayIndexNode = t.node

        if isinstance(self.evaluate_with_runner(t, expression.index_expression), ArithRef):
            print("Array index is an ArithRef")

        array_expr = get_z3_value(self.evaluate_with_runner(t, expression.arr_expression))
        index_expr = get_z3_value(self.evaluate_with_runner(t, expression.index_expression))
        return array_expr[index_expr]
