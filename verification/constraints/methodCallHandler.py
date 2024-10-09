from definitions.ast.methodCallNode import MethodCallNode
from nodes.baseNodeHandler import BaseNodeHandler
from verification.constraints.constraintsDto import ConstraintsDto


class MethodCallHandler(BaseNodeHandler[ConstraintsDto]):

    def is_node(self, t: ConstraintsDto):
        return isinstance(t.node, MethodCallNode)

    def handle(self, t: ConstraintsDto):
        raise Exception("Method call expression not supported")
