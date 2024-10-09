from definitions.ast.arrayLengthNode import ArrayLengthNode
from nodes.baseNodeHandler import BaseNodeHandler
from parser.simplifier.simplifierDto import SimplifierDto


class LengthSimplifier(BaseNodeHandler[SimplifierDto]):
    def is_node(self, t: SimplifierDto):
        return t.rule.getChildCount() == 3 and t.rule.children[1].getText() == '.' and t.rule.children[
            2].getText() == 'length'

    def handle(self, t: SimplifierDto):
        arr_expr = t.rule_simplifier.evaluate(SimplifierDto(t.rule.children[0], t.rule_simplifier, t.parser_result))
        return ArrayLengthNode(arr_expr)
