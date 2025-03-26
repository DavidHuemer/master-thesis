from definitions.ast.questionMarkNode import QuestionMarkNode
from nodes.baseNodeHandler import BaseNodeHandler
from parser.simplificationDto import SimplificationDto


class QuestionMarkExpressionSimplifier(BaseNodeHandler[SimplificationDto]):

    def is_node(self, t: SimplificationDto):
        return ((hasattr(t.node, 'question_mark') and t.node.question_mark is not None) and
                (hasattr(t.node, 'expr') and t.node.expr is not None) and
                (hasattr(t.node, 'true_expr') and t.node.true_expr is not None) and
                (hasattr(t.node, 'false_expr') and t.node.false_expr is not None))

    def handle(self, t: SimplificationDto):
        expr = self.evaluate_with_runner(t, t.node.expr)
        true_expr = self.evaluate_with_runner(t, t.node.true_expr)
        false_expr = self.evaluate_with_runner(t, t.node.false_expr)

        return QuestionMarkNode(expr, true_expr, false_expr)
