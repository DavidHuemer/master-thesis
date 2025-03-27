import jpype
from jpype import java
from z3 import ArrayRef, SeqRef, Length

from definitions.ast.arrayLengthNode import ArrayLengthNode
from nodes.baseNodeHandler import BaseNodeHandler
from verification.resultVerification.range.rangeDto import RangeDto


class LengthRangeHandler(BaseNodeHandler[RangeDto]):

    def is_node(self, t: RangeDto):
        return isinstance(t.node, ArrayLengthNode)

    def handle(self, t: RangeDto):
        expression: ArrayLengthNode = t.node
        expr = self.evaluate_with_runner(t, expression.arr_expr)

        if isinstance(expr, jpype.JArray):
            return len(expr)

        if isinstance(expr, list):
            return len(expr)

        if isinstance(expr, ArrayRef):
            return t.get_range_parameters().csp_parameters[str(expr)].length_param

        # Check if the expression is a java.lang.String
        if isinstance(expr, java.lang.String):
            return len(expr)

        if isinstance(expr, SeqRef):
            return Length(expr)

        raise Exception("Array length not found")
