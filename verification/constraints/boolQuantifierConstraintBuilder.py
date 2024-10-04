import copy

from z3 import Int, And, ForAll, Implies, Exists

from definitions.ast.quantifier.boolQuantifierTreeNode import BoolQuantifierTreeNode
from definitions.ast.quantifier.boolQuantifierType import BoolQuantifierType
from definitions.evaluations.csp.cspParameter import CSPParameter
from definitions.evaluations.csp.jmlProblem import JMLProblem
from definitions.evaluations.csp.parameters.jmlParameters import JmlParameters
from verification.constraints.quantifier.quantifierRangeValuesHelper import QuantifierRangeValuesHelper
from verification.constraints.quantifierConstraintBuilder import QuantifierConstraintBuilder


class BoolQuantifierConstraintBuilder:
    def __init__(self, quantifier_constraint_builder=QuantifierConstraintBuilder,
                 quantifier_range_values_helper=QuantifierRangeValuesHelper()):
        self.quantifier_constraint_builder = quantifier_constraint_builder()
        self.quantifier_range_values_helper = quantifier_range_values_helper

    def evaluate(self, jml_problem: JMLProblem, parameters: JmlParameters, expression: BoolQuantifierTreeNode,
                 constraint_builder):
        from verification.constraints.expressionConstraintBuilder import ExpressionConstraintBuilder
        constraint_builder: ExpressionConstraintBuilder = constraint_builder

        # First get variables
        variables = self.quantifier_range_values_helper.get_variables(expression)
        copied_jml_parameters = copy.deepcopy(parameters)

        for var in variables:
            copied_jml_parameters.csp_parameters[var] = variables[var]

        range_expressions = (self.quantifier_constraint_builder.get_range_expressions(
            jml_problem=jml_problem,
            range_=expression.range_,
            parameters=copied_jml_parameters,
            constraint_builder=constraint_builder))

        variable_values = [variables[var].value for var in variables]

        # TODO: Add support for additional expression in range
        and_implies = And(*range_expressions)

        final_expr = constraint_builder.build_expression_constraint(jml_problem,
                                                                    copied_jml_parameters,
                                                                    expression.expression)

        if expression.quantifier_type == BoolQuantifierType.FORALL:
            return self.evaluate_for_all(variable_values, and_implies, final_expr)
        elif expression.quantifier_type == BoolQuantifierType.EXISTS:
            return self.evaluate_exists(variable_values, and_implies, final_expr)

        raise Exception("BoolQuantifierConstraintBuilder: Quantifier type not supported")

    @staticmethod
    def evaluate_for_all(variable_values, range_, expr):
        return ForAll(*variable_values, Implies(range_, expr))

    @staticmethod
    def evaluate_exists(variable_values, range_, expr):
        return Exists(*variable_values, And(range_, expr))
