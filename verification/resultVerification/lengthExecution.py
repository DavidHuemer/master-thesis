from definitions.ast.arrayLengthNode import ArrayLengthNode
from nodes.baseNodeHandler import BaseNodeHandler
from verification.resultVerification.resultDto import ResultDto


class LengthExecution(BaseNodeHandler[ResultDto]):
    def is_node(self, t: ResultDto):
        return isinstance(t.node, ArrayLengthNode)

    def handle(self, t: ResultDto):
        expression: ArrayLengthNode = t.node
        eval_expr = self.evaluate_with_runner(t, expression.arr_expr)
        return len(eval_expr)
