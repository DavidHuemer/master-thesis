import parser.generated.JMLParser as JMLParser

from definitions.ast.methodCallNode import MethodCallNode
from helper.objectHelper import ObjectHelper
from nodes.baseNodeHandler import BaseNodeHandler
from parser.simplificationDto import SimplificationDto


class MethodCallSimplifier(BaseNodeHandler[SimplificationDto]):

    def is_node(self, t: SimplificationDto):
        return (isinstance(t.node, JMLParser.JMLParser.Method_callContext)
                and ObjectHelper.check_has_child(t.node, "ident")
                and ObjectHelper.check_has_child(t.node, "args"))

    def handle(self, t: SimplificationDto):
        ident = t.node.ident.text
        args = self.get_args(t)

        return MethodCallNode(ident, args)

    def get_args(self, t: SimplificationDto):
        arguments_expr = t.node.args
        if not ObjectHelper.check_has_child(arguments_expr, "expressions"):
            return []
        else:
            return self.get_arg_expressions(arguments_expr.expressions, t)

    @staticmethod
    def get_arg_expressions(expressions_list_expr: JMLParser.JMLParser.ExpressionListContext, t: SimplificationDto):
        # Filter real expressions
        real_expressions = list(filter(lambda x: isinstance(x, JMLParser.JMLParser.ExpressionContext),
                                       expressions_list_expr.children))

        simplified_expressions = [t.evaluate_with_other_node(expr) for expr in real_expressions]
        return simplified_expressions
