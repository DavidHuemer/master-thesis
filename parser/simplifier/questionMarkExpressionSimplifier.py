import parser.generated.JMLParser as JMLParser
from definitions.ast.questionMarkNode import QuestionMarkNode


class QuestionMarkExpressionSimplifier:
    @staticmethod
    def is_question_mark_expression(rule):
        return isinstance(rule, JMLParser.JMLParser.Question_mark_expressionContext)

    @staticmethod
    def simplify(rule, parser_result, simplifier):
        if not isinstance(rule, JMLParser.JMLParser.Question_mark_expressionContext):
            return None

        expr = simplifier.simplify_rule(rule.expr, parser_result)
        true_expr = simplifier.simplify_rule(rule.true_val, parser_result)
        false_expr = simplifier.simplify_rule(rule.false_val, parser_result)

        return QuestionMarkNode(expr, true_expr, false_expr)
