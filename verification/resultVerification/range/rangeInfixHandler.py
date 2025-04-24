from definitions.ast.infixExpression import InfixExpression
from helper.infixHelper import InfixHelper
from nodes.baseNodeHandler import BaseNodeHandler
from verification.resultVerification.range.rangeDto import RangeDto


class RangeInfixHandler(BaseNodeHandler[RangeDto]):
    def __init__(self, infix_helper=None):
        super().__init__()
        self.infix_helper = infix_helper or InfixHelper()

    def is_node(self, t: RangeDto):
        return isinstance(t.node, InfixExpression)

    def handle(self, t: RangeDto):
        expression: InfixExpression = t.node
        return self.infix_helper.evaluate_infix(infix_operator=expression.name,
                                                left=lambda: self.evaluate_with_runner(t, expression.left),
                                                right=lambda: self.evaluate_with_runner(t, expression.right),
                                                is_smt=True,
                                                csp_parameters=t.get_range_parameters().csp_parameters)
