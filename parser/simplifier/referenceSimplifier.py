import parser.generated.JMLParser as JMLParser

from definitions.ast.astTreeNode import AstTreeNode
from helper.objectHelper import ObjectHelper


class ReferenceSimplifier:
    """
    Simplifies references like \\old and \\this
    """

    def simplify(self, rule, parser_result, rule_simplifier):
        old_expr = self.simplify_old(rule, parser_result, rule_simplifier)
        if old_expr is not None:
            return old_expr

        this_expr = self.simplify_this(rule, parser_result, rule_simplifier)
        if this_expr is not None:
            return this_expr

        return None

    def simplify_old(self, rule, parser_result, rule_simplifier) -> AstTreeNode | None:
        from parser.simplifier.rule_simplifier import RuleSimplifier
        rule_simplifier: RuleSimplifier = rule_simplifier

        if (not isinstance(rule, JMLParser.JMLParser.Old_expressionContext) or
                not ObjectHelper.check_has_child(rule, "expr")):
            return None

        expr = rule_simplifier.simplify_rule(rule.expr, parser_result)
        # Set for all expressions that they are old
        self.set_old(expr)
        return expr

    @staticmethod
    def simplify_this(rule, parser_result, rule_simplifier):
        from parser.simplifier.rule_simplifier import RuleSimplifier
        rule_simplifier: RuleSimplifier = rule_simplifier

        if not (isinstance(rule, JMLParser.JMLParser.This_expressionContext) or
                not ObjectHelper.check_has_child(rule, "expr")):
            return None

        expr = rule_simplifier.simplify_rule(rule.expr, parser_result)
        expr.use_this = True
        return expr

    def set_old(self, expr: AstTreeNode):
        """
        Sets the old flag for all children of the expression
        :param expr: The node to set the old flag for
        """
        for child in expr.children:
            self.set_old(child)
