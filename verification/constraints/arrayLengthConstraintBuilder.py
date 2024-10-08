from z3 import ArrayRef, SeqRef, Length

from definitions.ast.arrayLengthNode import ArrayLengthNode
from definitions.ast.astTreeNode import AstTreeNode
from definitions.evaluations.csp.jmlProblem import JMLProblem
from definitions.evaluations.csp.parameters.cspParamHelperType import CSPParamHelperType
from definitions.evaluations.csp.parameters.jmlParameters import JmlParameters


class ArrayLengthConstraintBuilder:
    @staticmethod
    def is_array_length(expression: AstTreeNode):
        return isinstance(expression, ArrayLengthNode)

    @staticmethod
    def handle_array_length(expression: ArrayLengthNode, jml_problem: JMLProblem, jml_parameters: JmlParameters,
                            expression_constraint_builder):
        from verification.constraints.expressionConstraintBuilder import ExpressionConstraintBuilder
        expression_constraint_builder: ExpressionConstraintBuilder = expression_constraint_builder
        expr = expression_constraint_builder.build_expression_constraint(jml_problem, jml_parameters, expression.arr_expr)

        if isinstance(expr, ArrayRef):
            length_param = jml_parameters.csp_parameters.get_helper(str(expr), CSPParamHelperType.LENGTH)
            return length_param.value
        elif isinstance(expr, SeqRef):
            return Length(expr)

        raise Exception("Array length expression not supported")
