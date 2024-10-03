from definitions.ast.astTreeNode import AstTreeNode
from definitions.ast.infixExpression import InfixExpression


class RangeTreeNode(AstTreeNode):
    def __init__(self, name: str, start: InfixExpression, end: InfixExpression, start_operator: str, end_operator: str):
        super().__init__("Range")
        self.name = name
        self.start = start
        self.end = end
        self.start_operator = start_operator
        self.end_operator = end_operator

        self.children = [start, end]

    def get_tree_string(self):
        return f'Range: {self.start.get_tree_string()} - {self.end.get_tree_string()}'
