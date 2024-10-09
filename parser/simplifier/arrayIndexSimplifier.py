from definitions.ast.arrayIndexNode import ArrayIndexNode
from helper.objectHelper import ObjectHelper
from nodes.baseNodeHandler import BaseNodeHandler
from parser.simplifier.simplifierDto import SimplifierDto


class ArrayIndexSimplifier(BaseNodeHandler[SimplifierDto]):

    def is_node(self, t: SimplifierDto):
        return (t.rule.getChildCount() == 4
                and ObjectHelper.check_child_text(t.rule, 1, '[')
                and ObjectHelper.check_child_text(t.rule, 3, ']')
                and ObjectHelper.check_has_child(t.rule, "expr")
                and ObjectHelper.check_has_child(t.rule, "index_expr"))

    def handle(self, t: SimplifierDto):
        expr = t.rule_simplifier.evaluate(SimplifierDto(t.rule.expr, t.rule_simplifier, t.parser_result))
        index_expr = t.rule_simplifier.evaluate(SimplifierDto(t.rule.index_expr, t.rule_simplifier, t.parser_result))
        return ArrayIndexNode(expr, index_expr)
