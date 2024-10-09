from antlr4.tree.Tree import TerminalNodeImpl

from nodes.baseNodeHandler import BaseNodeHandler
from parser.simplifier.simplifierDto import SimplifierDto
from definitions.ast.terminalNode import TerminalNode


class TerminalSimplifier(BaseNodeHandler[SimplifierDto]):

    def is_node(self, t: SimplifierDto):
        return isinstance(t.rule, TerminalNodeImpl)

    def handle(self, t: SimplifierDto):
        return TerminalNode(t.parser_result.jml_parser.symbolicNames[t.rule.getSymbol().type], t.rule.getText())
