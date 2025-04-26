from definitions.ast.astTreeNode import AstTreeNode
from definitions.evaluations.csp.jmlProblem import JMLProblem
from definitions.parameters.Variables import Variables
from testGeneration.constraints.constraintsBuilder import build_constraints


def build_jml_problem(variables: Variables, expressions: list[AstTreeNode]) -> JMLProblem:
    """
    Builds a JML problem from the given method information and expressions.
    :param variables: The parameters of the method
    :param expressions: The expressions that are required for the initial constraints
    :return:
    """

    jml_problem = JMLProblem(variables)
    build_constraints(jml_problem, expressions)
    return jml_problem
