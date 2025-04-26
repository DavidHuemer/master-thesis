import parser.generated.JMLParser as JMLParser

from definitions.ast.exceptionExpression import ExceptionExpression
from nodes.baseNodeHandler import BaseNodeHandler
from parser.simplificationDto import SimplificationDto


class ExceptionSimplifier(BaseNodeHandler[SimplificationDto]):

    def is_node(self, t: SimplificationDto):
        return isinstance(t.node, JMLParser.JMLParser.Exception_expressionContext)

    def handle(self, t: SimplificationDto):
        # Check declaration and expr
        exception_type, exception_name = self.get_declaration(t.node)

        if not hasattr(t.node, "expr"):
            raise Exception("Exception node must have an expression")

        expr = t.node.expr
        simplified_expr = self.evaluate_with_runner(t, expr)
        return ExceptionExpression(exception_type, exception_name, simplified_expr)

    @staticmethod
    def get_declaration(rule: JMLParser.JMLParser.Exception_expressionContext):
        if not hasattr(rule, "declaration"):
            raise Exception("Exception node must have a declaration")

        declaration_expr = rule.declaration

        # Check that declaration expr must have 4 children
        if not hasattr(declaration_expr, "exception"):
            raise Exception("Exception declaration must have a exception")

        if not hasattr(declaration_expr, "name") or declaration_expr.name is None:
            name = "e"
        else:
            name = declaration_expr.name.text

        exception_expr = declaration_expr.exception
        return exception_expr.text, name
