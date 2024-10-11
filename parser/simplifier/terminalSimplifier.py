from antlr4.tree.Tree import TerminalNodeImpl

from definitions.ast.terminalNode import TerminalNode
from nodes.baseNodeHandler import BaseNodeHandler
from parser.simplificationDto import SimplificationDto


class TerminalSimplifier(BaseNodeHandler[SimplificationDto]):

    def is_node(self, t: SimplificationDto):
        return isinstance(t.node, TerminalNodeImpl)

    def handle(self, t: SimplificationDto):
        return TerminalNode(t.parser_result.jml_parser.symbolicNames[t.node.getSymbol().type], t.node.getText())
