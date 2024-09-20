from definitions.ast.astTreeNode import AstTreeNode


class ExceptionExpression(AstTreeNode):
    def __init__(self, exception_type: str, exception_name: str, expression: AstTreeNode):
        super().__init__(exception_type)
        self.exception_type = exception_type
        self.exception_name = exception_name
        self.expression = expression

    def get_tree_string(self):
        return f'{self.exception_type} {self.exception_name} {self.expression.get_tree_string()}'

    def __str__(self):
        return self.get_tree_string()
