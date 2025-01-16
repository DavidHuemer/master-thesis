from z3 import ExprRef

from definitions.ast.terminalNode import TerminalNode
from definitions.evaluations.csp.parameters.constraintParameters import ConstraintParameters
from definitions.evaluations.exceptions.preConditionException import PreConditionException
from nodes.baseNodeHandler import BaseNodeHandler
from testGeneration.constraints.constraintsDto import ConstraintsDto


class TerminalConstraintBuilder(BaseNodeHandler[ConstraintsDto]):

    def is_node(self, t: ConstraintsDto):
        return isinstance(t.node, TerminalNode)

    def handle(self, t: ConstraintsDto):
        terminal_node: TerminalNode = t.node

        if terminal_node.name == "INTEGER":
            return int(terminal_node.value)
        elif terminal_node.name == "IDENTIFIER":
            param_key = terminal_node.value
            return self.evaluate_variable(param_key, t.constraint_parameters)
        elif terminal_node.name == "BOOL_LITERAL":
            return terminal_node.value == "true"
        elif terminal_node.name == "NULL":
            return t.constraint_parameters.csp_parameters.is_null_helper_param.value
        elif terminal_node.name == "RESULT":
            raise PreConditionException("\\result not supported in pre conditions")

        raise PreConditionException(f"Terminal node {terminal_node.name} not supported in pre conditions")

    @staticmethod
    def evaluate_variable(variable_name: str, parameters: ConstraintParameters) -> ExprRef:
        if parameters.parameter_exists(variable_name):
            return parameters.get_parameter_by_key(variable_name, use_old=False, use_this=False).value
        else:
            raise Exception(f"Variable {variable_name} not found in parameters")
