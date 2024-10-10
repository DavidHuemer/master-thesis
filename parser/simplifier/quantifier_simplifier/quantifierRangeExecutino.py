from definitions.ast.quantifier.boolQuantifierTreeNode import BoolQuantifierTreeNode
from definitions.ast.quantifier.numQuantifierTreeNode import NumQuantifierTreeNode
from nodes.baseNodeHandler import BaseNodeHandler
from verification.resultVerification.range.rangeDto import RangeDto


class QuantifierRangeExecution(BaseNodeHandler[RangeDto]):
    def is_node(self, t: RangeDto):
        return isinstance(t.node, BoolQuantifierTreeNode) or isinstance(t.node, NumQuantifierTreeNode)

    def handle(self, t: RangeDto):
        raise Exception("QuantifierRangeExecution: Node type not supported")
