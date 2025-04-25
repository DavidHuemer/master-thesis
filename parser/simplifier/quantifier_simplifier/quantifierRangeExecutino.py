from definitions.ast.quantifier.boolQuantifierTreeNode import BoolQuantifierTreeNode
from definitions.ast.quantifier.numQuantifierTreeNode import NumQuantifierTreeNode
from nodes.baseNodeHandler import BaseNodeHandler
from verification.resultVerification.resultDto import ResultDto


class QuantifierRangeExecution(BaseNodeHandler[ResultDto]):
    def is_node(self, t: ResultDto):
        return isinstance(t.node, BoolQuantifierTreeNode) or isinstance(t.node, NumQuantifierTreeNode)

    def handle(self, t: ResultDto):
        raise Exception("A quantifier inside the range of another quantifier is not supported")
