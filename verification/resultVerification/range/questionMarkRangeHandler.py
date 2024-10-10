from z3 import If

from definitions.ast.questionMarkNode import QuestionMarkNode
from nodes.baseNodeHandler import BaseNodeHandler
from verification.resultVerification.range.rangeDto import RangeDto


class QuestionMarkRangeHandler(BaseNodeHandler[RangeDto]):
    def is_node(self, t: RangeDto):
        return isinstance(t.node, QuestionMarkNode)

    def handle(self, t: RangeDto):
        expression: QuestionMarkNode = t.node
        expr = t.constraint_builder.evaluate(t.copy_with_other_node(expression.expr))
        true_expr = t.constraint_builder.evaluate(t.copy_with_other_node(expression.true_expr))
        false_expr = t.constraint_builder.evaluate(t.copy_with_other_node(expression.false_expr))
        return If(expr, true_expr, false_expr)
