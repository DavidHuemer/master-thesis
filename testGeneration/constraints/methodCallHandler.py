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

    def handle_obj_method(self, t: ConstraintsDto, method: MethodCallNode):
        obj = self.evaluate_with_runner(t, method.obj)
        ident = method.name

        if not hasattr(obj, ident):
            raise Exception(f"Method {ident} not found in object {obj}")

        m = getattr(obj, ident)
        if not m:
            raise Exception(f"Method {ident} not found in object {obj}")

        return m(*[self.evaluate_with_runner(t, arg) for arg in method.args])

    def handle_static_method(self, method: MethodCallNode):
        raise Exception("Not implemented yet")
