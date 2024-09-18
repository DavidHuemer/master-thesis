from definitions.ast.expressionNode import ExpressionNode
from definitions.evaluations.csp.jmlProblem import JMLProblem
from definitions.javaMethod import JavaMethod
from verification.constraints.constraintsBuilder import ConstraintsBuilder
from verification.csp.cspParamBuilder import CSPParameterBuilder


class JMLProblemBuilder:
    """
    Helper class to build JML problems from method information and expressions.
    """

    def __init__(self, csp_param_builder=CSPParameterBuilder(), constraints_builder=ConstraintsBuilder()):
        self.csp_param_builder = csp_param_builder
        self.constraints_builder = constraints_builder

    def build(self, method_info: JavaMethod, expressions: list[ExpressionNode]) -> JMLProblem:
        """
        Builds a JML problem from the given method information and expressions.
        :param method_info: The java method that should be tested
        :param expressions: The expressions that are required for the initial constraints
        :return:
        """
        parameters = self.csp_param_builder.build_parameters(method_info)
        jml_problem = JMLProblem(parameters)
        self.constraints_builder.build_constraints(jml_problem, expressions)
        return jml_problem
