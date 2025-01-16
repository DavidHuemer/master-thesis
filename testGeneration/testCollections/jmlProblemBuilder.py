from definitions.ast.astTreeNode import AstTreeNode
from definitions.code.parameterExtractionInfo import ParameterExtractionInfo
from definitions.evaluations.csp.jmlProblem import JMLProblem
from definitions.evaluations.csp.parameters.jmlParameters import JmlParameters
from testGeneration.constraints.constraintsBuilder import build_constraints
from verification.csp.cspParamBuilder import build_csp_parameters


def build_jml_problem(parameters: list[ParameterExtractionInfo], expressions: list[AstTreeNode]) -> JMLProblem:
    """
    Builds a JML problem from the given method information and expressions.
    :param parameters: The parameters of the method
    :param expressions: The expressions that are required for the initial constraints
    :return:
    """

    csp_parameters = build_csp_parameters(parameters)

    jml_parameters = JmlParameters(csp_parameters)
    jml_problem = JMLProblem(jml_parameters)
    build_constraints(jml_problem, expressions)
    return jml_problem
