from definitions.ast.arrayIndexNode import ArrayIndexNode
from nodes.baseNodeHandler import BaseNodeHandler
from verification.resultVerification.range.rangeDto import RangeDto


class ArrayIndexRangeHandler(BaseNodeHandler[RangeDto]):
    def is_node(self, t: RangeDto):
        return isinstance(t.node, ArrayIndexNode)

    def handle(self, t: RangeDto):
        expr: ArrayIndexNode = t.node
        expression = t.constraint_builder.evaluate(t.copy_with_other_node(expr.arr_expression))
        index = t.constraint_builder.evaluate(t.copy_with_other_node(expr.index_expression))
        return expression[index]
