from z3 import Not

from definitions.ast.prefixNode import PrefixNode
from definitions.evaluations.csp.jmlProblem import JMLProblem
from definitions.evaluations.csp.parameters.jmlParameters import JmlParameters


class PrefixConstraintBuilder:
    @staticmethod
    def evaluate(prefix_expression: PrefixNode, jml_problem: JMLProblem, jml_parameters: JmlParameters,
                 expression_constraint_builder):
        from verification.constraints.expressionConstraintBuilder import ExpressionConstraintBuilder
        expression_constraint_builder: ExpressionConstraintBuilder = expression_constraint_builder
        if prefix_expression.prefix == '++':
            return expression_constraint_builder.build_expression_constraint(jml_problem,
                                                                             jml_parameters,
                                                                             prefix_expression.expr) + 1
        elif prefix_expression.prefix == '--':
            return expression_constraint_builder.build_expression_constraint(jml_problem,
                                                                             jml_parameters,
                                                                             prefix_expression.expr) - 1
        elif prefix_expression.prefix == '!':
            return Not(expression_constraint_builder.build_expression_constraint(jml_problem,
                                                                                 jml_parameters,
                                                                                 prefix_expression.expr))
        elif prefix_expression.prefix == '+':
            return expression_constraint_builder.build_expression_constraint(jml_problem,
                                                                             jml_parameters,
                                                                             prefix_expression.expr)
        elif prefix_expression.prefix == '-':
            return -expression_constraint_builder.build_expression_constraint(jml_problem,
                                                                              jml_parameters,
                                                                              prefix_expression.expr)
        elif prefix_expression.prefix == '~':
            return ~expression_constraint_builder.build_expression_constraint(jml_problem,
                                                                              jml_parameters,
                                                                              prefix_expression.expr)

        raise Exception(f"Unsupported prefix: {prefix_expression.prefix}")
