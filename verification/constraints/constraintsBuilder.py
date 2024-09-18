from definitions.ast.expressionNode import ExpressionNode
from definitions.evaluations.csp.cspParameter import CSPParameter
from definitions.evaluations.csp.jmlProblem import JMLProblem
from verification.constraints.typeConstraintBuilder import TypeConstraintBuilder


class ConstraintsBuilder:
    def __init__(self, type_constraint_builder=TypeConstraintBuilder()):
        self.type_constraint_builder = type_constraint_builder

    def build_constraints(self, jml_problem: JMLProblem, expressions: list[ExpressionNode]):
        # Steps for building constraints:

        # Add type related constraints (e.g. min value for int, etc.)
        self.add_type_constraints(jml_problem)

        # Add constraints for each expression
        # TODO: Add expressions to the JMLProblem
        pass

    def add_type_constraints(self, jml_problem: JMLProblem):
        for param_key in jml_problem.parameters:
            param: CSPParameter = jml_problem.parameters[param_key]
            self.type_constraint_builder.build_type_constraint(jml_problem, param)

        pass
