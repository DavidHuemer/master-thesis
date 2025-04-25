import jpype
from jpype import java
from z3 import ArrayRef, SeqRef, Length

from definitions.ast.arrayLengthNode import ArrayLengthNode
from definitions.evaluations.csp.cspParameter import CSPParameter
from nodes.baseNodeHandler import BaseNodeHandler
from verification.resultVerification.resultDto import ResultDto


class LengthRangeHandler(BaseNodeHandler[ResultDto]):

    def is_node(self, t: ResultDto):
        return isinstance(t.node, ArrayLengthNode)

    def handle(self, t: ResultDto):
        expression: ArrayLengthNode = t.node
        expr = self.evaluate_with_runner(t, expression.arr_expr)

        if isinstance(expr, jpype.JArray):
            return len(expr)

        if isinstance(expr, list):
            return len(expr)

        if isinstance(expr, CSPParameter):
            if expr.param_type == "String":
                return Length(expr.value)

            return expr.length_param

        if isinstance(expr, ArrayRef):
            return t.get_result_parameters().csp_parameters[str(expr)].length_param

        # Check if the expression is a java.lang.String
        if isinstance(expr, java.lang.String):
            return len(expr)

        if isinstance(expr, SeqRef):
            return Length(expr)

        raise Exception("Array length not found")
