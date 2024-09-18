from definitions.ast.astTreeNode import AstTreeNode
from definitions.ast.expressionNode import ExpressionNode


class JmlTreeNode(AstTreeNode):
    def __init__(self):
        super().__init__("JML")
        self.pre_conditions: list[ExpressionNode] = []
        self.post_conditions: list[ExpressionNode] = []

    def add_pre_condition(self, pre_condition: ExpressionNode):
        self.pre_conditions.append(pre_condition)

    def add_post_condition(self, expr):
        self.post_conditions.append(expr)

    def get_tree_string(self):
        return f'{self.name} ({self.get_conditions_string(self.pre_conditions)}) -> ({self.get_conditions_string(self.post_conditions)})'

    def get_conditions_string(self, conditions: list[ExpressionNode]):
        return f'{",".join([x.get_tree_string() for x in conditions])}'

    def __str__(self):
        return self.get_tree_string()
