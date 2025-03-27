from z3 import ArrayRef, SeqRef, Length

from definitions.ast.arrayLengthNode import ArrayLengthNode
from definitions.evaluations.csp.parameters.cspParamHelperType import CSPParamHelperType
from nodes.baseNodeHandler import BaseNodeHandler
from testGeneration.constraints.constraintsDto import ConstraintsDto


class ArrayLengthConstraintBuilder(BaseNodeHandler[ConstraintsDto]):
    def is_node(self, t: ConstraintsDto):
        return isinstance(t.node, ArrayLengthNode)

    def handle(self, t: ConstraintsDto):
        parent_expr: ArrayLengthNode = t.node
        expr = self.evaluate_with_runner(t, parent_expr.arr_expr)

        if isinstance(expr, ArrayRef):
            return t.constraint_parameters.csp_parameters[str(expr)].length_param
        elif isinstance(expr, SeqRef):
            return Length(expr)
