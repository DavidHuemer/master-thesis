from definitions.ast.questionMarkNode import QuestionMarkNode
from nodes.baseNodeHandler import BaseNodeHandler
from verification.resultVerification.resultDto import ResultDto


class QuestionMarkExecution(BaseNodeHandler[ResultDto]):
    def is_node(self, t: ResultDto):
        return isinstance(t.node, QuestionMarkNode)

    def handle(self, t: ResultDto):
        expression: QuestionMarkNode = t.node
        expr_result = t.result_verifier.evaluate(t.copy_with_other_node(expression.expr))

        if expr_result:
            return t.result_verifier.evaluate(t.copy_with_other_node(expression.true_expr))
        else:
            return t.result_verifier.evaluate(t.copy_with_other_node(expression.false_expr))
