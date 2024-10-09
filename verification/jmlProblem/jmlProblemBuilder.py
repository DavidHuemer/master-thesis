from definitions.ast.astTreeNode import AstTreeNode
from definitions.code.parameterExtractionInfo import ParameterExtractionInfo
from definitions.evaluations.csp.jmlProblem import JMLProblem
from definitions.evaluations.csp.parameters.jmlParameters import JmlParameters
from verification.constraints.constraintsBuilder import ConstraintsBuilder
from verification.csp.cspParamBuilder import CSPParameterBuilder


class JMLProblemBuilder:
    """
    Helper class to build JML problems from method information and expressions.
    """

    def __init__(self, csp_param_builder=CSPParameterBuilder(), constraints_builder=ConstraintsBuilder()):
        self.csp_param_builder = csp_param_builder
        self.constraints_builder = constraints_builder

    def build(self, parameters: list[ParameterExtractionInfo], expressions: list[AstTreeNode]) -> JMLProblem:
        """
        Builds a JML problem from the given method information and expressions.
        :param parameters: The parameters of the method
        :param expressions: The expressions that are required for the initial constraints
        :return:
        """

        csp_parameters = self.csp_param_builder.build_csp_parameters(parameters)

        jml_parameters = JmlParameters(csp_parameters)
        jml_problem = JMLProblem(jml_parameters)
        self.constraints_builder.build_constraints(jml_problem, expressions)
        return jml_problem
