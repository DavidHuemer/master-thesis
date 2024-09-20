from definitions.ast.astTreeNode import AstTreeNode
from definitions.evaluations.csp.cspParameter import CSPParameter
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

        # Add type related constraints (e.g. min value for int, etc.)
        self.add_type_constraints(jml_problem)

        # Add constraints for each expression
        self.add_expression_constraints(jml_problem, expressions)
        pass

    def add_type_constraints(self, jml_problem: JMLProblem):
        for param_key in jml_problem.parameters:
            param: CSPParameter = jml_problem.parameters[param_key]
            self.type_constraint_builder.build_type_constraint(jml_problem, param)

        pass

    def add_expression_constraints(self, jml_problem: JMLProblem, expressions: list[AstTreeNode]):
        for expression in expressions:
            constraint = self.expression_constraint_builder.build_expression_constraint(jml_problem, expression)
            jml_problem.add_constraint(constraint)
