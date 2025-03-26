from definitions.ast.arrayIndexNode import ArrayIndexNode
from definitions.evaluations.BaseDto import BaseDto
from nodes.baseNodeHandler import BaseNodeHandler


class BaseArrayIndexConstraintBuilder(BaseNodeHandler[BaseDto]):
    def is_node(self, t: BaseDto):
        return isinstance(t.node, ArrayIndexNode)

    def handle(self, t: BaseDto):
        expression: ArrayIndexNode = t.node
        array_expr = self.evaluate_with_runner(t, expression.arr_expression)
        index_expr = self.evaluate_with_runner(t, expression.index_expression)
        return array_expr[index_expr]
