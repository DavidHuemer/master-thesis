import parser.generated.JMLParser as JMLParser
from definitions.ast.exceptionExpression import ExceptionExpression
from nodes.baseNodeHandler import BaseNodeHandler

from parser.simplifier.simplifierDto import SimplifierDto


class ExceptionSimplifier(BaseNodeHandler[SimplifierDto]):

    def is_node(self, t: SimplifierDto):
        return isinstance(t.rule, JMLParser.JMLParser.Exception_expressionContext)

    def handle(self, t: SimplifierDto):
        # Check declaration and expr
        exception_type, exception_name = self.get_declaration(t.rule)

        if not hasattr(t.rule, "expr"):
            raise Exception("Exception node must have an expression")

        expr = t.rule.expr
        simplified_expr = t.rule_simplifier.evaluate(SimplifierDto(expr, t.rule_simplifier, t.parser_result))
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
