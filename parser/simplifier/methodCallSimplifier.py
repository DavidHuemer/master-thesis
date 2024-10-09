import parser.generated.JMLParser as JMLParser

from definitions.ast.methodCallNode import MethodCallNode
from helper.objectHelper import ObjectHelper
from nodes.baseNodeHandler import BaseNodeHandler
from parser.simplifier.simplifierDto import SimplifierDto


class MethodCallSimplifier(BaseNodeHandler[SimplifierDto]):

    def is_node(self, t: SimplifierDto):
        return (isinstance(t.rule, JMLParser.JMLParser.Method_callContext)
                and not ObjectHelper.check_has_child(t.rule, "ident")
                and not ObjectHelper.check_has_child(t.rule, "args"))

    def handle(self, t: SimplifierDto):
        ident = t.rule.ident.text
        args = self.get_args(t)

        return MethodCallNode(ident, args)

    def get_args(self, t: SimplifierDto):
        arguments_expr = t.rule.args
        if not ObjectHelper.check_has_child(arguments_expr, "expressions"):
            return []
        else:
            return self.get_arg_expressions(arguments_expr.expressions, t)

    @staticmethod
    def get_arg_expressions(expressions_list_expr: JMLParser.JMLParser.ExpressionListContext, t: SimplifierDto):
        # Filter real expressions
        real_expressions = list(filter(lambda x: isinstance(x, JMLParser.JMLParser.ExpressionContext),
                                       expressions_list_expr.children))

        simplified_expressions = [t.rule_simplifier.evaluate(SimplifierDto(expr, t.rule_simplifier, t.parser_result))
                                  for expr in real_expressions]
        return simplified_expressions
