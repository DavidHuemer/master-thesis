from __future__ import annotations

from definitions.ast.astTreeNode import AstTreeNode


class ExpressionNode(AstTreeNode):
    def __init__(self, name: str):
        super().__init__(name)
        self.children = []

    def add_child(self, child: AstTreeNode):
        self.children.append(child)

    def get_tree_string(self):
        return f'{self.name} ({",".join([x.get_tree_string() for x in self.children])})'
