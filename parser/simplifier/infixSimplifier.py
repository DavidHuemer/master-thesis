from parser.generated.JMLParser import JMLParser

from definitions.ast.infixExpression import InfixExpression
from nodes.baseNodeHandler import BaseNodeHandler
from parser.simplificationDto import SimplificationDto


class InfixSimplifier(BaseNodeHandler[SimplificationDto]):
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

    def is_node(self, t: SimplificationDto):
        rule = t.node
        return (hasattr(rule, "left") and rule.left is not None
                and hasattr(rule, "right") and rule.right is not None and
                hasattr(rule, "op") and rule.op is not None)

    def handle(self, t: SimplificationDto):
        left = t.evaluate_with_other_node(t.node.left)
        right = t.evaluate_with_other_node(t.node.right)

        if self.is_relational(t.node.op.text):
            if isinstance(left, InfixExpression) and self.is_relational(left.name):
                return InfixExpression("&&", left, InfixExpression(t.node.op.text, left.right, right))

        return InfixExpression(t.node.op.text, left, right)

    @staticmethod
    def is_relational(op: str):
        return op in ["<", ">", "<=", ">="]
