import copy

from z3 import Int, And, ForAll, Implies, Exists

from definitions.ast.quantifier.boolQuantifierTreeNode import BoolQuantifierTreeNode
from definitions.ast.quantifier.boolQuantifierType import BoolQuantifierType
from definitions.evaluations.csp.cspParameter import CSPParameter
from definitions.evaluations.csp.jmlProblem import JMLProblem
from verification.constraints.quantifierConstraintBuilder import QuantifierConstraintBuilder


class BoolQuantifierConstraintBuilder:
    def __init__(self, quantifier_constraint_builder=QuantifierConstraintBuilder):
        self.quantifier_constraint_builder = quantifier_constraint_builder()

    def evaluate(self, parameters: dict[str, CSPParameter], expression: BoolQuantifierTreeNode, constraint_builder,
                 jml_problem: JMLProblem):
        # First get variables
        variables = self.get_variables(expression)
        copied_parameters = copy.deepcopy(parameters)

        # Add variables to parameters
        copied_parameters.update(variables)

        range_expressions = (self.quantifier_constraint_builder
                             .get_range_expressions(range_=expression.range_,
                                                    parameters=copied_parameters,
                                                    constraint_builder=constraint_builder))

        variable_values = [variables[var].value for var in variables]

        # TODO: Add support for additional expression in range
        and_implies = And(*range_expressions)

        final_expr = constraint_builder.build_expression_constraint(copied_parameters, expression.expression,
                                                                    jml_problem)

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

    def get_variables(self, expression: BoolQuantifierTreeNode):
        variables = dict()

        for variable in expression.variable_names:
            var_type = variable[0]
            var_name = variable[1]

            # TODO: Add support for other variable types
            variables[var_name] = CSPParameter(var_name, Int(var_name), var_type, True)

        return variables
