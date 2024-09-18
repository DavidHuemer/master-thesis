from definitions.ast.astTreeNode import AstTreeNode


class InfixExpression(AstTreeNode):
    def __init__(self, name: str, left: AstTreeNode, right: AstTreeNode):
        super().__init__(name)
        self.left = left
        self.right = right

    def get_tree_string(self):
        return f"{self.name} ({self.left.get_tree_string()}, {self.right.get_tree_string()})"

