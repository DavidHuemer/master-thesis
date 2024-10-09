import parser.generated.JMLParser as JMLParser

from definitions.ast.astTreeNode import AstTreeNode
from nodes.baseNodeHandler import BaseNodeHandler
from parser.simplifier.simplifierDto import SimplifierDto


class ReferenceSimplifier(BaseNodeHandler[SimplifierDto]):
    """
    Simplifies references like \\old and \\this
    """

    def is_node(self, t: SimplifierDto):
        return (self.is_old_expression(t) or
                self.is_this_expression(t))

    @staticmethod
    def is_old_expression(t: SimplifierDto):
        return isinstance(t.rule, JMLParser.JMLParser.Old_expressionContext)

    @staticmethod
    def is_this_expression(t: SimplifierDto):
        return isinstance(t.rule, JMLParser.JMLParser.This_expressionContext)

    def handle(self, t: SimplifierDto):
        if self.is_old_expression(t):
            return self.simplify_old(t)
        elif self.is_this_expression(t):
            return self.simplify_this(t)

        raise Exception("ReferenceSimplifier: Rule is not a reference expression")

    def simplify_old(self, t: SimplifierDto) -> AstTreeNode | None:
        expr = t.rule_simplifier.evaluate(SimplifierDto(t.rule.expr, t.rule_simplifier, t.parser_result))
        # Set for all expressions that they are old
        self.set_old(expr)
        return expr

    @staticmethod
    def simplify_this(t: SimplifierDto):
        expr = t.rule_simplifier.evaluate(SimplifierDto(t.rule.expr, t.rule_simplifier, t.parser_result))
        expr.use_this = True
        return expr

    def set_old(self, expr: AstTreeNode):
        """
        Sets the old flag for all children of the expression
        :param expr: The node to set the old flag for
        """
        for child in expr.children:
            self.set_old(child)
