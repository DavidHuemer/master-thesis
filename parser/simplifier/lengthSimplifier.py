from definitions.ast.arrayLengthNode import ArrayLengthNode
from nodes.baseNodeHandler import BaseNodeHandler
from parser.simplificationDto import SimplificationDto


class LengthSimplifier(BaseNodeHandler[SimplificationDto]):
    def is_node(self, t: SimplificationDto):
        return t.node.getChildCount() == 3 and t.node.children[1].getText() == '.' and t.node.children[
            2].getText() == 'length'

    def handle(self, t: SimplificationDto):
        arr_expr = t.evaluate_with_other_node(t.node.children[0])
        return ArrayLengthNode(arr_expr)
