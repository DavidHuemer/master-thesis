from definitions.ast.arrayIndexNode import ArrayIndexNode
from helper.objectHelper import ObjectHelper
from nodes.baseNodeHandler import BaseNodeHandler
from parser.simplificationDto import SimplificationDto


class ArrayIndexSimplifier(BaseNodeHandler[SimplificationDto]):

    def is_node(self, t: SimplificationDto):
        return (t.node.getChildCount() == 4
                and ObjectHelper.check_child_text(t.node, 1, '[')
                and ObjectHelper.check_child_text(t.node, 3, ']')
                and ObjectHelper.check_has_child(t.node, "expr")
                and ObjectHelper.check_has_child(t.node, "index_expr"))

    def handle(self, t: SimplificationDto):
        expr = t.evaluate_with_other_node(t.node.expr)
        index_expr = t.evaluate_with_other_node(t.node.index_expr)
        return ArrayIndexNode(expr, index_expr)
