from definitions.ast.infixExpression import InfixExpression
from parser.generated.JMLParser import JMLParser

from nodes.baseNodeHandler import BaseNodeHandler
from parser.simplifier.simplifierDto import SimplifierDto


class InfixSimplifier(BaseNodeHandler[SimplifierDto]):
    def simplify_infix(self, rule, parser_result, rule_simplifier):
        if self.is_infix_expression(rule):
            left = rule_simplifier.simplify_rule(rule.left, parser_result)
            right = rule_simplifier.simplify_rule(rule.right, parser_result)

            if isinstance(left, JMLParser.ExpressionContext):
                print("error")

            return InfixExpression(rule.op.text, left, right)

        return None

    @staticmethod
    def is_infix_expression(rule):
        return (hasattr(rule, "left") and rule.left is not None
                and hasattr(rule, "right") and rule.right is not None and
                hasattr(rule, "op") and rule.op is not None)

    def is_node(self, t: SimplifierDto):
        rule = t.rule
        return (hasattr(rule, "left") and rule.left is not None
                and hasattr(rule, "right") and rule.right is not None and
                hasattr(rule, "op") and rule.op is not None)

    def handle(self, t: SimplifierDto):
        left = t.rule_simplifier.evaluate(SimplifierDto(t.rule.left, t.rule_simplifier, t.parser_result))
        right = t.rule_simplifier.evaluate(SimplifierDto(t.rule.right, t.rule_simplifier, t.parser_result))

        return InfixExpression(t.rule.op.text, left, right)
