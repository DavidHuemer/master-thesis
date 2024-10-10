from z3 import ArrayRef

from definitions.ast.arrayLengthNode import ArrayLengthNode
from definitions.evaluations.csp.parameters.cspParamHelperType import CSPParamHelperType
from nodes.baseNodeHandler import BaseNodeHandler
from verification.resultVerification.range.rangeDto import RangeDto


class LengthRangeHandler(BaseNodeHandler[RangeDto]):

    def is_node(self, t: RangeDto):
        return isinstance(t.node, ArrayLengthNode)

    def handle(self, t: RangeDto):
        expression: ArrayLengthNode = t.node
        expr = t.constraint_builder.evaluate(t.copy_with_other_node(expression.arr_expr))

        if isinstance(expr, list):
            return len(expr)

        if isinstance(expr, ArrayRef):
            length_param = t.get_range_parameters().csp_parameters.get_helper(str(expr), CSPParamHelperType.LENGTH)
            return length_param.value

        raise Exception("Array length not found")
