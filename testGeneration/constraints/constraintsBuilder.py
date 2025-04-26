from definitions.ast.astTreeNode import AstTreeNode
from definitions.evaluations.csp.jmlProblem import JMLProblem
from testGeneration.constraints.constraintsDto import ConstraintsDto
from testGeneration.constraints.expressionConstraintBuilder import ExpressionConstraintBuilder
from testGeneration.constraints.typeConstraintBuilder import build_type_constraint


# TODO: Increase performance
def build_constraints(jml_problem: JMLProblem, expressions: list[AstTreeNode]):
    # Steps for building constraints:

    add_special_constraints(jml_problem)

    # Add type related constraints (e.g. min value for int, etc.)
    add_type_constraints(jml_problem)

    # Add constraints for each expression
    add_expression_constraints(jml_problem, expressions)


def add_special_constraints(jml_problem: JMLProblem):
    is_null_param = jml_problem.variables.special_parameters.is_null_param
    jml_problem.add_constraint(is_null_param == True)


def add_type_constraints(jml_problem: JMLProblem):
    for param in jml_problem.variables.method_call_parameters:
        build_type_constraint(jml_problem, param)


# TODO: Increase performance
def add_expression_constraints(jml_problem: JMLProblem, expressions: list[AstTreeNode]):
    # constraint_parameters = ConstraintParameters(jml_problem.parameters.csp_parameters)

    for expression in expressions:
        expr_constraint_builder = ExpressionConstraintBuilder()

        constraints_dto = ConstraintsDto(node=expression,
                                         jml_problem=jml_problem)
        constraint = expr_constraint_builder.evaluate(constraints_dto)
        jml_problem.add_constraint(constraint)
