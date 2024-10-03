from z3 import ExprRef

from definitions.ast.terminalNode import TerminalNode
from definitions.evaluations.csp.parameters.jmlParameters import JmlParameters
from definitions.evaluations.exceptions.preConditionException import PreConditionException


class TerminalConstraintBuilder:
    def evaluate_terminal_node(self, terminal_node: TerminalNode, parameters: JmlParameters):
        if terminal_node.name == "INTEGER":
            return int(terminal_node.value)
        elif terminal_node.name == "IDENTIFIER":
            param_key = terminal_node.value
            return self.evaluate_variable(param_key, parameters)
        elif terminal_node.name == "BOOL_LITERAL":
            return terminal_node.value == "true"
        elif terminal_node.name == "NULL":
            return parameters.csp_parameters.is_null_helper_param.value
        elif terminal_node.name == "RESULT":
            raise PreConditionException("\\result not supported in pre conditions")
        else:
            return None

    @staticmethod
    def evaluate_variable(variable_name: str, parameters: JmlParameters) -> ExprRef:
        if parameters.csp_parameters.parameter_exists(variable_name):
            return parameters.csp_parameters[variable_name].value
        else:
            raise Exception(f"Variable {variable_name} not found in parameters")
