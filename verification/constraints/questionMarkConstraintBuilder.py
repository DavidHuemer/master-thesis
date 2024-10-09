from z3 import If

from definitions.ast.questionMarkNode import QuestionMarkNode
from nodes.baseNodeHandler import BaseNodeHandler
from verification.constraints.constraintsDto import ConstraintsDto


class QuestionMarkConstraintBuilder(BaseNodeHandler[ConstraintsDto]):

    def is_node(self, t: ConstraintsDto):
        return isinstance(t.node, QuestionMarkNode)

    def handle(self, t: ConstraintsDto):
        question_mark_expr: QuestionMarkNode = t.node
        question_expr = t.constraint_builder.evaluate(t.copy_with_other_node(question_mark_expr.expr))
        true_expr = t.constraint_builder.evaluate(t.copy_with_other_node(question_mark_expr.true_expr))
        false_expr = t.constraint_builder.evaluate(t.copy_with_other_node(question_mark_expr.false_expr))

        return If(question_expr, true_expr, false_expr)
