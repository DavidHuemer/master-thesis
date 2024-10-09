from definitions.ast.infixExpression import InfixExpression
from helper.infixHelper import InfixHelper
from nodes.baseNodeHandler import BaseNodeHandler
from verification.resultVerification.resultDto import ResultDto


class InfixExecution(BaseNodeHandler[ResultDto]):
    def __init__(self, infix_helper=InfixHelper()):
        super().__init__()
        self.infix_helper = infix_helper

    def is_node(self, t: ResultDto):
        return isinstance(t.node, InfixExpression)

    def handle(self, t: ResultDto):
        expression: InfixExpression = t.node
        return self.infix_helper.evaluate_infix(infix_operator=expression.name,
                                                left=lambda: t.result_verifier.evaluate(
                                                    t.copy_with_other_node(expression.left)),
                                                right=lambda: t.result_verifier.evaluate(
                                                    t.copy_with_other_node(expression.right)),
                                                csp_parameters=None, is_smt=False)
