from definitions.ast.infixExpression import InfixExpression
from helper.infixHelper import InfixHelper
from nodes.baseNodeHandler import BaseNodeHandler
from verification.resultVerification.resultDto import ResultDto


class InfixExecution(BaseNodeHandler[ResultDto]):
    def __init__(self, infix_helper=None):
        super().__init__()
        self.infix_helper = infix_helper or InfixHelper()

    def is_node(self, t: ResultDto):
        return isinstance(t.node, InfixExpression)

    def handle(self, t: ResultDto):
        expression: InfixExpression = t.node
        return self.infix_helper.evaluate_infix(infix_operator=expression.name,
                                                left=lambda: self.evaluate_with_runner(t, expression.left),
                                                right=lambda: self.evaluate_with_runner(t, expression.right),
                                                csp_parameters=None, is_smt=False)
