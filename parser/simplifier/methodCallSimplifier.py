import parser.generated.JMLParser as JMLParser

from definitions.ast.methodCallNode import MethodCallNode
from helper.objectHelper import ObjectHelper
from nodes.baseNodeHandler import BaseNodeHandler
from parser.simplificationDto import SimplificationDto


class MethodCallSimplifier(BaseNodeHandler[SimplificationDto]):

    def is_node(self, t: SimplificationDto):
        return self.is_static_method(t) or self.is_object_method(t)

    @staticmethod
    def is_static_method(t: SimplificationDto):
        """
        Check if the node is a method call

        A static method does mean the method is called without an object instance
        :param t: SimplificationDto
        :return: Whether the node is a static method call
        """
        return (isinstance(t.node, JMLParser.JMLParser.Method_callContext)
                and ObjectHelper.check_has_child(t.node, "ident")
                and ObjectHelper.check_has_child(t.node, "args"))

    @staticmethod
    def is_object_method(t: SimplificationDto):
        return (ObjectHelper.check_has_child(t.node, "expr")
                and ObjectHelper.check_has_child(t.node, "method"))

    def handle(self, t: SimplificationDto):
        if self.is_static_method(t):
            return self.handle_static_method(t)
        else:
            return self.handle_object_method(t)

    def handle_static_method(self, t: SimplificationDto):
        ident = t.node.ident.text
        args = self.get_args(t)

        return MethodCallNode(ident, args)

    def handle_object_method(self, t: SimplificationDto):
        method_t = SimplificationDto(t.node.method, t.runner, t.parser_result)

        ident = method_t.node.ident.text
        args = self.get_args(method_t)

        obj = t.evaluate_with_other_node(t.node.expr)
        return MethodCallNode(ident, args, obj)

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
