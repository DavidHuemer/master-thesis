from antlr4.Token import CommonToken

from definitions.ast.prefixNode import PrefixNode
from nodes.baseNodeHandler import BaseNodeHandler
from parser.simplificationDto import SimplificationDto


class PrefixSimplifier(BaseNodeHandler[SimplificationDto]):

    def is_node(self, t: SimplificationDto):
        return hasattr(t.node, "prefix") and t.node.prefix is not None and isinstance(t.node.prefix, CommonToken)

    def handle(self, t: SimplificationDto):
        prefix = t.node.prefix.text
        expr = t.evaluate_with_other_node(t.node.expr)
        return PrefixNode(prefix, expr)
