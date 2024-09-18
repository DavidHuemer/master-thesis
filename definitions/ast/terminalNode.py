from definitions.ast.astTreeNode import AstTreeNode


class TerminalNode(AstTreeNode):
    def __init__(self, name: str, value):
        super().__init__(name)
        self.value = value

    def get_tree_string(self):
        return f'{self.name} value={self.value}'
