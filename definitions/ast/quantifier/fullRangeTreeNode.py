from definitions.ast.RangeTreeNode import RangeTreeNode
from definitions.ast.expressionNode import ExpressionNode


class FullRangeTreeNode:
    def __init__(self, ranges: list[RangeTreeNode], expr: ExpressionNode | None):
        self.ranges = ranges
        self.expr = expr
