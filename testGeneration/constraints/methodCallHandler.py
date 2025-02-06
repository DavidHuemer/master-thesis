from definitions.ast.methodCallNode import MethodCallNode
from nodes.baseNodeHandler import BaseNodeHandler
from testGeneration.constraints.constraintsDto import ConstraintsDto
from verification.resultVerification.resultDto import ResultDto


class MethodCallHandler(BaseNodeHandler[ConstraintsDto]):

    def is_node(self, t: ConstraintsDto):
        return isinstance(t.node, MethodCallNode)

    def handle(self, t: ConstraintsDto):
        method: MethodCallNode = t.node

        if method.obj:
            return self.handle_obj_method(t, method)
        else:
            return self.handle_static_method(method)

    @staticmethod
    def handle_obj_method(t: ResultDto, method: MethodCallNode):
        obj = t.evaluate_with_other_node(method.obj)
        ident = method.name

        m = getattr(obj, ident)
        if not m:
            raise Exception(f"Method {ident} not found in object {obj}")

        return m(*[t.evaluate_with_other_node(arg) for arg in method.args])

    def handle_static_method(self, method: MethodCallNode):
        raise Exception("Not implemented yet")
