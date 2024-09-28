import parser.generated.JMLParser as JMLParser
from definitions.ast.questionMarkNode import QuestionMarkNode


class QuestionMarkExpressionSimplifier:
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
