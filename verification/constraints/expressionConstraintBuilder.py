from z3 import And, Or, Bool

from definitions.ast.arrayIndexNode import ArrayIndexNode
from definitions.ast.arrayLengthNode import ArrayLengthNode
from definitions.ast.astTreeNode import AstTreeNode
from definitions.ast.infixExpression import InfixExpression
from definitions.ast.terminalNode import TerminalNode
from definitions.evaluations.csp.jmlProblem import JMLProblem


class ExpressionConstraintBuilder:
    def build_expression_constraint(self, jml_problem: JMLProblem, expression: AstTreeNode):
        if isinstance(expression, InfixExpression):
            return self.build_infix_expression(jml_problem, expression)

        # TODO: Include all supported expression types
        if isinstance(expression, ArrayIndexNode):
            array_param = jml_problem.parameters[expression.name]
            expr = self.build_expression_constraint(jml_problem, expression.expression)
            return array_param.value[expr]

        if isinstance(expression, ArrayLengthNode):
            array_length_param_key = expression.name + "_length"
            array_length_param = jml_problem.parameters[array_length_param_key]
            return array_length_param.value

        if isinstance(expression, TerminalNode):
            return self.evaluate_terminal_node(jml_problem, expression)

        return None

    def build_infix_expression(self, jml_problem: JMLProblem, expression: InfixExpression):
        left = self.build_expression_constraint(jml_problem, expression.left)
        right = self.build_expression_constraint(jml_problem, expression.right)

        # TODO: Add additional infix operators
        if expression.name == "+":
            return left + right
        elif expression.name == "-":
            return left - right
        elif expression.name == "*":
            return left * right
        elif expression.name == "/":
            return left / right
        elif expression.name == "<":
            return left < right
        elif expression.name == "<=":
            return left <= right
        elif expression.name == ">":
            return left > right
        elif expression.name == ">=":
            return left >= right
        elif expression.name == "==":
            return left == right
        elif expression.name == "!=":
            return left != right
        elif expression.name == "&&":
            return And(left, right)
        elif expression.name == "||":
            return Or(left, right)

        raise Exception("ExpressionConstraintBuilder: Infix expression not supported")

    def evaluate_terminal_node(self, jml_problem: JMLProblem, terminal: TerminalNode):
        if terminal.name == "INTEGER":
            return int(terminal.value)
        elif terminal.name == "IDENTIFIER":
            param_key = terminal.value
            if param_key in jml_problem.parameters:
                return jml_problem.parameters[param_key].value
            else:
                return None
        elif terminal.name == "BOOL_LITERAL":
            return terminal.value == "true"
        elif terminal.name == "NULL":
            return Bool("is_null")
        else:
            return None
