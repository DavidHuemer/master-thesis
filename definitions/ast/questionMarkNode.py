from definitions.ast.astTreeNode import AstTreeNode


class QuestionMarkNode(AstTreeNode):
    def __init__(self, expr, true_expr, false_expr):
        super().__init__("QuestionMarkNode")
        self.expr = expr
        self.true_expr = true_expr
        self.false_expr = false_expr

        self.children = [expr, true_expr, false_expr]
