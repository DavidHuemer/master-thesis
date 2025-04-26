from typing import cast

from z3 import If

from definitions.ast.questionMarkNode import QuestionMarkNode
from definitions.evaluations.BaseDto import BaseDto
from nodes.baseNodeHandler import BaseNodeHandler


class BaseQuestionMarkConstraintBuilder(BaseNodeHandler[BaseDto]):

    def is_node(self, t: BaseDto):
        return isinstance(t.node, QuestionMarkNode)

    def handle(self, t: BaseDto):
        question_mark_expr: QuestionMarkNode = cast(QuestionMarkNode, t.node)
        question_expr = self.evaluate_with_runner(t, question_mark_expr.expr)
        true_expr = self.evaluate_with_runner(t, question_mark_expr.true_expr)
        false_expr = self.evaluate_with_runner(t, question_mark_expr.false_expr)

        return If(question_expr, true_expr, false_expr)
