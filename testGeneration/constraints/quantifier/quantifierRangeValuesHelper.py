from z3 import Int

from definitions.ast.quantifier.quantifierTreeNode import QuantifierTreeNode
from definitions.evaluations.csp.cspParameter import CSPParameter


class QuantifierRangeValuesHelper:
    @staticmethod
    def get_variables(expression: QuantifierTreeNode) -> list[CSPParameter]:
        """
        Returns a list of variables that are declared in a quantified node
        :param expression: The quantified node
        :return: A list of variables
        """
        variables = list()

        for variable in expression.variable_names:
            var_type = variable[0]
            var_name = variable[1]

            # TODO: Add support for other variable types
            csp_parameter = CSPParameter(var_name, Int(var_name), var_type, True)
            variables.append(csp_parameter)

        return variables
