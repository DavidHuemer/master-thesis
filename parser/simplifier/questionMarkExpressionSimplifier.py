from definitions.ast.questionMarkNode import QuestionMarkNode
from nodes.baseNodeHandler import BaseNodeHandler
from parser.simplifier.simplifierDto import SimplifierDto


class QuestionMarkExpressionSimplifier(BaseNodeHandler[SimplifierDto]):

    def is_node(self, t: SimplifierDto):
        return ((hasattr(t.rule, 'question_mark') and t.rule.question_mark is not None) and
                (hasattr(t.rule, 'expr') and t.rule.expr is not None) and
                (hasattr(t.rule, 'true_expr') and t.rule.true_expr is not None) and
                (hasattr(t.rule, 'false_expr') and t.rule.false_expr is not None))

    def handle(self, t: SimplifierDto):
        expr = t.rule_simplifier.evaluate(SimplifierDto(t.rule.expr, t.rule_simplifier, t.parser_result))
        true_expr = t.rule_simplifier.evaluate(SimplifierDto(t.rule.true_expr, t.rule_simplifier, t.parser_result))
        false_expr = t.rule_simplifier.evaluate(SimplifierDto(t.rule.false_expr, t.rule_simplifier, t.parser_result))

        return QuestionMarkNode(expr, true_expr, false_expr)

    @staticmethod
    def is_question_mark_expression(rule):
        return ((hasattr(rule, 'question_mark') and rule.question_mark is not None) and
                (hasattr(rule, 'expr') and rule.expr is not None) and
                (hasattr(rule, 'true_expr') and rule.true_expr is not None) and
                (hasattr(rule, 'false_expr') and rule.false_expr is not None))

    def simplify(self, rule, parser_result, simplifier):
        if not self.is_question_mark_expression(rule):
            return None

        expr = simplifier.simplify_rule(rule.expr, parser_result)
        true_expr = simplifier.simplify_rule(rule.true_expr, parser_result)
        false_expr = simplifier.simplify_rule(rule.false_expr, parser_result)

        return QuestionMarkNode(expr, true_expr, false_expr)
