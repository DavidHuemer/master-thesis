from definitions.ast.infixExpression import InfixExpression
from helper.infixHelper import InfixHelper
from nodes.baseNodeHandler import BaseNodeHandler
from testGeneration.constraints.constraintsDto import ConstraintsDto


class InfixConstraintBuilder(BaseNodeHandler[ConstraintsDto]):
    def __init__(self, infix_helper=InfixHelper()):
        super().__init__()
        self.infix_helper = infix_helper

    def is_node(self, t: ConstraintsDto):
        return isinstance(t.node, InfixExpression) and hasattr(t.node, "left") and hasattr(t.node, "right")

    def handle(self, t: ConstraintsDto):
        expression: InfixExpression = t.node
        return self.infix_helper.evaluate_infix(infix_operator=expression.name,
                                                left=lambda: self.evaluate_with_runner(t, expression.left),
                                                right=lambda: self.evaluate_with_runner(t, expression.right),
                                                is_smt=True,
                                                csp_parameters=t.constraint_parameters.csp_parameters)
