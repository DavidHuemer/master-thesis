from definitions.ast.astTreeNode import AstTreeNode
from definitions.ast.behavior.behaviorType import BehaviorType
from definitions.ast.exceptionExpression import ExceptionExpression
from definitions.ast.expressionNode import ExpressionNode


class BehaviorNode(AstTreeNode):
    def __init__(self):
        super().__init__("BehaviorNode")
        self.behavior_type: BehaviorType = BehaviorType.DEFAULT
        self.defined = False

        self.pre_conditions: list[ExpressionNode] = []
        self.post_conditions: list[ExpressionNode] = []
        self.signals_conditions: list[ExceptionExpression] = []

    def add_pre_condition(self, pre_condition: ExpressionNode):
        self.pre_conditions.append(pre_condition)

    def add_post_condition(self, expr):
        self.post_conditions.append(expr)

    def add_signals_condition(self, expr: ExceptionExpression):
        self.signals_conditions.append(expr)

    def get_tree_string(self):
        return (f'{self.name} ({self.get_conditions_string(self.pre_conditions)}) '
                f'-> ({self.get_conditions_string(self.post_conditions)})')

    @staticmethod
    def get_conditions_string(conditions: list[AstTreeNode]):
        return f'{",".join([x.get_tree_string() for x in conditions])}'
