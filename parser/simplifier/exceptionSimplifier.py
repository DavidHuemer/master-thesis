import parser.generated.JMLParser as JMLParser
from definitions.ast.exceptionExpression import ExceptionExpression


class ExceptionSimplifier:
    def simplify(self, rule, parser_result, rule_simplifier):
        if not isinstance(rule, JMLParser.JMLParser.Exception_expressionContext):
            return None

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
        if not hasattr(declaration_expr, "exception"):
            raise Exception("Exception declaration must have a exception")

        if not hasattr(declaration_expr, "name") or declaration_expr.name is None:
            name = "e"
        else:
            name = declaration_expr.name.text

        exception_expr = declaration_expr.exception
        return exception_expr.text, name
