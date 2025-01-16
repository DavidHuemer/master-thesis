from definitions.ast.infixExpression import InfixExpression
from helper.infixHelper import InfixHelper
from nodes.baseNodeHandler import BaseNodeHandler
from testGeneration.constraints.constraintsDto import ConstraintsDto


class InfixConstraintBuilder(BaseNodeHandler[ConstraintsDto]):
    def __init__(self, infix_helper=InfixHelper()):
        self.infix_helper = infix_helper

    def is_node(self, t: ConstraintsDto):
        return isinstance(t.node, InfixExpression) and hasattr(t.node, "left") and hasattr(t.node, "right")

    def handle(self, t: ConstraintsDto):
        expression: InfixExpression = t.node
        return self.infix_helper.evaluate_infix(infix_operator=expression.name,
                                                left=lambda: t.constraint_builder.evaluate(
                                                    t.copy_with_other_node(expression.left)),
                                                right=lambda: t.constraint_builder.evaluate(
                                                    t.copy_with_other_node(expression.right)),
                                                is_smt=True,
                                                csp_parameters=t.constraint_parameters.csp_parameters)
