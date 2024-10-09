from antlr4.Token import CommonToken

from definitions.ast.prefixNode import PrefixNode
from nodes.baseNodeHandler import BaseNodeHandler
from parser.simplifier.simplifierDto import SimplifierDto


class PrefixSimplifier(BaseNodeHandler[SimplifierDto]):

    def is_node(self, t: SimplifierDto):
        return hasattr(t.rule, "prefix") and t.rule.prefix is not None and isinstance(t.rule.prefix, CommonToken)

    def handle(self, t: SimplifierDto):
        prefix = t.rule.prefix.text
        expr = t.rule_simplifier.evaluate(SimplifierDto(t.rule.expr, t.rule_simplifier, t.parser_result))
        return PrefixNode(prefix, expr)
