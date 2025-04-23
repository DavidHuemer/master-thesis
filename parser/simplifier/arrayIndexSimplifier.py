from definitions.ast.arrayIndexNode import ArrayIndexNode
from definitions.ast.methodCallNode import MethodCallNode
from helper.objectHelper import ObjectHelper
from nodes.baseNodeHandler import BaseNodeHandler
from parser.simplificationDto import SimplificationDto

from parser.generated import JMLParser


class ArrayIndexSimplifier(BaseNodeHandler[SimplificationDto]):

    def is_node(self, t: SimplificationDto):
        return self.is_array_node(t) or self.is_string_node(t)

    @staticmethod
    def is_array_node(t: SimplificationDto):
        return (t.node.getChildCount() == 4
                and ObjectHelper.check_child_text(t.node, 1, '[')
                and ObjectHelper.check_child_text(t.node, 3, ']')
                and ObjectHelper.check_has_child(t.node, "expr")
                and ObjectHelper.check_has_child(t.node, "index_expr"))

    @staticmethod
    def is_string_node(t: SimplificationDto):
        return (t.node.getChildCount() == 3
                and ObjectHelper.check_child_text(t.node, 1, '.')
                and isinstance(t.node.getChild(2), JMLParser.JMLParser.Method_callContext)
                and ObjectHelper.check_child_text(t.node.getChild(2), 0, "charAt"))

    def handle(self, t: SimplificationDto):
        expr = self.evaluate_with_runner(t, t.node.expr)

        if self.is_array_node(t):
            index_expr = self.evaluate_with_runner(t, t.node.index_expr)
            return ArrayIndexNode(expr, index_expr)

        if self.is_string_node(t):
            method_expr = self.evaluate_with_runner(t, t.node.getChild(2))
            if not isinstance(method_expr, MethodCallNode):
                raise Exception("Method expression is not a MethodCallNode")

            if len(method_expr.args) != 1:
                raise Exception("Method expression does not have exactly one argument")

            return ArrayIndexNode(expr, method_expr.args[0])
