import parser.generated.JMLParser as JMLParser

from definitions.ast.methodCallNode import MethodCallNode
from helper.objectHelper import ObjectHelper


class MethodCallSimplifier:
    def __init__(self):
        pass

    def simplify(self, rule, parser_result, rule_simplifier):
        if (not isinstance(rule, JMLParser.JMLParser.Method_callContext)
                or not ObjectHelper.check_has_child(rule, "ident")
                or not ObjectHelper.check_has_child(rule, "args")):
            return None

        ident = rule.ident.text
        args = self.get_args(rule, parser_result, rule_simplifier)

        return MethodCallNode(ident, args)

    def get_args(self, rule: JMLParser.JMLParser.Method_callContext, parser_result, rule_simplifier):
        arguments_expr = rule.args
        if not ObjectHelper.check_has_child(arguments_expr, "expressions"):
            return []
        else:
            return self.get_arg_expressions(arguments_expr.expressions, parser_result, rule_simplifier)

    def get_arg_expressions(self, expressions_list_expr: JMLParser.JMLParser.ExpressionListContext, parser_result,
                            rule_simplifier):
        # Filter real expressions
        real_expressions = list(filter(lambda x: isinstance(x, JMLParser.JMLParser.ExpressionContext),
                                       expressions_list_expr.children))

        simplified_expressions = [rule_simplifier.simplify_rule(expr, parser_result) for expr in real_expressions]
        return simplified_expressions
