from antlr4.tree.Tree import TerminalNodeImpl

from definitions.ast.arrayLengthNode import ArrayLengthNode
from nodes.baseNodeHandler import BaseNodeHandler
from parser.simplificationDto import SimplificationDto
from parser.generated import JMLParser


class LengthSimplifier(BaseNodeHandler[SimplificationDto]):
    def is_node(self, t: SimplificationDto):
        return t.node.getChildCount() == 3 and t.node.children[1].getText() == '.' and (
                self.is_method_length(t) or self.is_array_length(t))

    def is_method_length(self, t: SimplificationDto):
        return isinstance(t.node.children[2], JMLParser.JMLParser.Method_callContext) and t.node.children[
            2].ident.text == 'length'

    def is_array_length(self, t: SimplificationDto):
        return isinstance(t.node.children[2],
                          TerminalNodeImpl) and t.node.children[2].getText() == 'length'


    def handle(self, t: SimplificationDto):
        arr_expr = t.evaluate_with_other_node(t.node.children[0])
        return ArrayLengthNode(arr_expr)
