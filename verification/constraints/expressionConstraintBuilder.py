from definitions.ast.arrayIndexNode import ArrayIndexNode
from definitions.ast.arrayLengthNode import ArrayLengthNode
from definitions.ast.astTreeNode import AstTreeNode
from definitions.ast.infixExpression import InfixExpression
from definitions.ast.quantifier.boolQuantifierTreeNode import BoolQuantifierTreeNode
from definitions.ast.terminalNode import TerminalNode
from definitions.evaluations.csp.cspParameter import CSPParameter
from definitions.evaluations.exceptions.preConditionException import PreConditionException
from helper.infixHelper import InfixHelper
from verification.constraints.boolQuantifierConstraintBuilder import BoolQuantifierConstraintBuilder


class ExpressionConstraintBuilder:
    def __init__(self, bool_quantifier_constraint_builder=BoolQuantifierConstraintBuilder(),
                 infix_helper=InfixHelper()):
        self.bool_quantifier_constraint_builder = bool_quantifier_constraint_builder
        self.infix_helper = infix_helper

    def build_expression_constraint(self, parameters: dict[str, CSPParameter], expression: AstTreeNode):
        if isinstance(expression, InfixExpression) and hasattr(expression, "left") and hasattr(expression, "right"):
            return self.infix_helper.evaluate_infix(infix_operator=expression.name,
                                                    left=lambda: self.build_expression_constraint(parameters,
                                                                                                  expression.left),
                                                    right=lambda: self.build_expression_constraint(parameters,
                                                                                                   expression.right),
                                                    is_smt=True,
                                                    get_param=lambda name: parameters[name])

        # TODO: Include all supported expression types
        if isinstance(expression, ArrayIndexNode):
            array_param = parameters[expression.name]
            expr = self.build_expression_constraint(parameters, expression.expression)
            return array_param.value[expr]

        if isinstance(expression, ArrayLengthNode):
            array_length_param_key = expression.name + "_length"
            array_length_param = parameters[array_length_param_key]
            return array_length_param.value

        if isinstance(expression, TerminalNode):
            return self.evaluate_terminal_node(parameters, expression)

        if isinstance(expression, BoolQuantifierTreeNode):
            return self.bool_quantifier_constraint_builder.evaluate(parameters, expression, self)

        raise Exception("ExpressionConstraintBuilder: Expression type not supported")

    def evaluate_terminal_node(self, parameters: dict[str, CSPParameter], terminal: TerminalNode):
        if terminal.name == "INTEGER":
            return int(terminal.value)
        elif terminal.name == "IDENTIFIER":
            param_key = terminal.value
            if param_key in parameters:
                return parameters[param_key].value
            else:
                return None
        elif terminal.name == "BOOL_LITERAL":
            return terminal.value == "true"
        elif terminal.name == "NULL":
            return parameters["is_null"].value
        elif terminal.name == "RESULT":
            raise PreConditionException("\\result not supported in pre conditions")
        else:
            return None
