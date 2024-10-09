from definitions.ast.methodCallNode import MethodCallNode
from nodes.baseNodeHandler import BaseNodeHandler
from verification.resultVerification.resultDto import ResultDto


class MethodCallExecution(BaseNodeHandler[ResultDto]):
    def is_node(self, t: ResultDto):
        return isinstance(t.node, MethodCallNode)

    def handle(self, t: ResultDto):
        raise Exception("Not implemented yet")
