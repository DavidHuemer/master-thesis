from z3 import ArrayRef, SeqRef, Length

from definitions.ast.arrayLengthNode import ArrayLengthNode
from definitions.evaluations.csp.parameters.cspParamHelperType import CSPParamHelperType
from nodes.baseNodeHandler import BaseNodeHandler
from verification.constraints.constraintsDto import ConstraintsDto


class ArrayLengthConstraintBuilder(BaseNodeHandler[ConstraintsDto]):
    def is_node(self, t: ConstraintsDto):
        return isinstance(t.node, ArrayLengthNode)

    def handle(self, t: ConstraintsDto):
        parent_expr: ArrayLengthNode = t.node
        expr = t.constraint_builder.evaluate(t.copy_with_other_node(parent_expr.arr_expr))

        if isinstance(expr, ArrayRef):
            length_param = t.constraint_parameters.csp_parameters.get_helper(str(expr), CSPParamHelperType.LENGTH)
            return length_param.value
        elif isinstance(expr, SeqRef):
            return Length(expr)
