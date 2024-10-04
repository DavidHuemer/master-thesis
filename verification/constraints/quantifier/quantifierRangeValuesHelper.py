import copy

from z3 import Int

from definitions.ast.quantifier.quantifierTreeNode import QuantifierTreeNode
from definitions.evaluations.csp.cspParameter import CSPParameter
from definitions.evaluations.csp.parameters.jmlParameters import JmlParameters


class QuantifierRangeValuesHelper:
    def handle_range_variables(self, expression: QuantifierTreeNode, jml_parameters: JmlParameters) \
            -> tuple[list[CSPParameter], JmlParameters]:
        variables = self.get_variables(expression)

        copied_jml_parameters = copy.deepcopy(jml_parameters)
        for var in variables:
            copied_jml_parameters.csp_parameters[var] = variables[var]

        return list(variables.values()), copied_jml_parameters

    @staticmethod
    def get_variables(expression: QuantifierTreeNode):
        variables = dict()

        for variable in expression.variable_names:
            var_type = variable[0]
            var_name = variable[1]

            # TODO: Add support for other variable types
            variables[var_name] = CSPParameter(var_name, Int(var_name), var_type, True)

        return variables
