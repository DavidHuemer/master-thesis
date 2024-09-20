import parser.generated.JMLParser as JMLParser
from definitions.ast.exceptionExpression import ExceptionExpression


class ExceptionSimplifier:
    def simplify(self, rule, parser_result, rule_simplifier):
        # Check declaration and expr
        exception_type, exception_name = self.get_declaration(rule)

        if not hasattr(rule, "expr"):
            raise Exception("Exception node must have an expression")

        expr = rule.expr
        simplified_expr = rule_simplifier.simplify_rule(expr, parser_result)
        return ExceptionExpression(exception_type, exception_name, simplified_expr)

    @staticmethod
    def get_declaration(rule: JMLParser.JMLParser.Exception_expressionContext):
        if not hasattr(rule, "declaration"):
            raise Exception("Exception node must have a declaration")

        declaration_expr = rule.declaration

        # Check that declaration expr must have 4 children
        if declaration_expr.getChildCount() != 4:
            raise Exception("Exception declaration must have 4 children")

        if not hasattr(declaration_expr, "exception"):
            raise Exception("Exception declaration must have a exception")

        if not hasattr(declaration_expr, "exception"):
            raise Exception("Exception declaration must have a name")

        exception_expr = declaration_expr.exception
        name_expr = declaration_expr.name

        return exception_expr.text, name_expr.text
