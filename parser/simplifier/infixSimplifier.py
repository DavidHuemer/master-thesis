from definitions.ast.infixExpression import InfixExpression


class InfixSimplifier:
    def simplify_infix(self, rule, parser_result, rule_simplifier):
        if self.is_infix_expression(rule):
            return InfixExpression(rule.op.text, rule_simplifier.simplify_rule(rule.left, parser_result),
                                   rule_simplifier.simplify_rule(rule.right, parser_result))

        return None

    @staticmethod
    def is_infix_expression(rule):
        return (hasattr(rule, "left") and rule.left is not None
                and hasattr(rule, "right") and rule.right is not None and
                hasattr(rule, "op") and rule.op is not None)
