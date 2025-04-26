from definitions.ast.questionMarkNode import QuestionMarkNode
from nodes.baseNodeHandler import BaseNodeHandler
from verification.resultVerification.resultDto import ResultDto


class QuestionMarkExecution(BaseNodeHandler[ResultDto]):
    def is_node(self, t: ResultDto):
        return isinstance(t.node, QuestionMarkNode)

    def handle(self, t: ResultDto):
        expression: QuestionMarkNode = t.node
        expr_result = self.evaluate_with_runner(t, expression.expr)

        if expr_result:
            return self.evaluate_with_runner(t, expression.true_expr)
        else:
            return self.evaluate_with_runner(t, expression.false_expr)
