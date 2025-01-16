from dependency_injector.wiring import inject, Provide

from definitions.ast.astTreeNode import AstTreeNode
from definitions.evaluations.csp.jmlProblem import JMLProblem
from definitions.evaluations.csp.parameters.constraintParameters import ConstraintParameters
from testGeneration.constraints import constraintsContainer
from testGeneration.constraints.constraintsContainer import ConstraintsContainer
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
    is_null_param = jml_problem.parameters.csp_parameters.is_null_helper_param
    jml_problem.add_constraint(is_null_param.value == True)


def add_type_constraints(jml_problem: JMLProblem):
    for param in jml_problem.parameters.csp_parameters.get_actual_parameters():
        build_type_constraint(jml_problem, param)


# TODO: Increase performance
@inject
def add_expression_constraints(jml_problem: JMLProblem, expressions: list[AstTreeNode],
                               expression_constraint_builder: ExpressionConstraintBuilder = Provide[
                                   ConstraintsContainer.expression_constraint_builder]):
    for expression in expressions:
        constraint_parameters = ConstraintParameters(jml_problem.parameters.csp_parameters)
        constraints_dto = ConstraintsDto(node=expression,
                                         jml_problem=jml_problem,
                                         constraint_builder=expression_constraint_builder,
                                         constraint_parameters=constraint_parameters)
        constraint = expression_constraint_builder.evaluate(constraints_dto)
        jml_problem.add_constraint(constraint)
