import parser.generated.JMLParser as JMLParser

from definitions.ast.astTreeNode import AstTreeNode
from nodes.baseNodeHandler import BaseNodeHandler
from parser.simplificationDto import SimplificationDto


class ReferenceSimplifier(BaseNodeHandler[SimplificationDto]):
    """
    Simplifies references like \\old and \\this
    """

    def is_node(self, t: SimplificationDto):
        return (self.is_old_expression(t) or
                self.is_this_expression(t))

    @staticmethod
    def is_old_expression(t: SimplificationDto):
        return isinstance(t.node, JMLParser.JMLParser.Old_expressionContext)

    @staticmethod
    def is_this_expression(t: SimplificationDto):
        return isinstance(t.node, JMLParser.JMLParser.This_expressionContext)

    def handle(self, t: SimplificationDto):
        if self.is_old_expression(t):
            return self.simplify_old(t)
        elif self.is_this_expression(t):
            return self.simplify_this(t)

        raise Exception("ReferenceSimplifier: Rule is not a reference expression")

    def simplify_old(self, t: SimplificationDto) -> AstTreeNode | None:
        expr = self.evaluate_with_runner(t, t.node.expr)
        # Set for all expressions that they are old
        self.set_old(expr)
        return expr

    def simplify_this(self, t: SimplificationDto):
        expr = self.evaluate_with_runner(t, t.node.expr)
        expr.use_this = True
        return expr

    def set_old(self, expr: AstTreeNode):
        """
        Sets the old flag for all children of the expression
        :param expr: The node to set the old flag for
        """

        expr.use_old = True

        for child in expr.children:
            self.set_old(child)
