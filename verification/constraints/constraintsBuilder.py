from z3 import And

from definitions.ast.astTreeNode import AstTreeNode
from definitions.evaluations.csp.jmlProblem import JMLProblem
from verification.constraints.expressionConstraintBuilder import ExpressionConstraintBuilder
from verification.constraints.typeConstraintBuilder import TypeConstraintBuilder


class ConstraintsBuilder:
    def __init__(self, type_constraint_builder=TypeConstraintBuilder(),
                 expression_constraint_builder=ExpressionConstraintBuilder()):
        self.type_constraint_builder = type_constraint_builder
        self.expression_constraint_builder = expression_constraint_builder

    def build_constraints(self, jml_problem: JMLProblem, expressions: list[AstTreeNode]):
        # Steps for building constraints:

        self.add_special_constraints(jml_problem)

        # Add type related constraints (e.g. min value for int, etc.)
        self.add_type_constraints(jml_problem)

        # Add constraints for each expression
        self.add_expression_constraints(jml_problem, expressions)

    @staticmethod
    def add_special_constraints(jml_problem: JMLProblem):
        is_null_param = jml_problem.parameters.csp_parameters.is_null_helper_param
        jml_problem.add_constraint(And(is_null_param.value, True))

    def add_type_constraints(self, jml_problem: JMLProblem):
        for param in jml_problem.parameters.csp_parameters.get_actual_parameters():
            self.type_constraint_builder.build_type_constraint(jml_problem, param)

    def add_expression_constraints(self, jml_problem: JMLProblem, expressions: list[AstTreeNode]):
        for expression in expressions:
            constraint = (self.expression_constraint_builder
                          .build_expression_constraint(jml_problem=jml_problem, expression=expression,
                                                       jml_parameters=jml_problem.parameters))
            jml_problem.add_constraint(constraint)
