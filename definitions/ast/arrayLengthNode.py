from definitions.ast.astTreeNode import AstTreeNode


class ArrayLengthNode(AstTreeNode):
    def __init__(self, name: str):
        super().__init__(name)
