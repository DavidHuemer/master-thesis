from definitions.ast.astTreeNode import AstTreeNode


class QuantifierTreeNode(AstTreeNode):
    def __init__(self, name: str, variable_names: list[tuple[str, str]] | None, full_range: AstTreeNode | None):
        super().__init__(name)
        self.variable_names = variable_names
        self.range_ = full_range
