from definitions.ast.arrayIndexNode import ArrayIndexNode
from definitions.ast.arrayLengthNode import ArrayLengthNode
from definitions.ast.astTreeNode import AstTreeNode
from definitions.ast.infixExpression import InfixExpression
from definitions.ast.quantifier.boolQuantifierTreeNode import BoolQuantifierTreeNode
from definitions.ast.quantifier.numQuantifierTreeNode import NumQuantifierTreeNode
from definitions.ast.terminalNode import TerminalNode
from definitions.evaluations.csp.cspParameter import CSPParameter
from definitions.evaluations.csp.jmlProblem import JMLProblem
from definitions.evaluations.exceptions.preConditionException import PreConditionException
from helper.infixHelper import InfixHelper
from verification.constraints.boolQuantifierConstraintBuilder import BoolQuantifierConstraintBuilder
from verification.constraints.numQuantifierConstraintBuilder import NumQuantifierConstraintBuilder


class ExpressionConstraintBuilder:
    def __init__(self, bool_quantifier_constraint_builder=BoolQuantifierConstraintBuilder(),
                 num_quantifier_constraint_builder=NumQuantifierConstraintBuilder(),
                 infix_helper=InfixHelper()):
        self.bool_quantifier_constraint_builder = bool_quantifier_constraint_builder
        self.infix_helper = infix_helper
        self.num_quantifier_constraint_builder = num_quantifier_constraint_builder

    def build_expression_constraint(self, parameters: dict[str, CSPParameter], expression: AstTreeNode,
                                    jml_problem: JMLProblem):
        if isinstance(expression, TerminalNode):
            return self.evaluate_terminal_node(parameters, expression)

        if isinstance(expression, BoolQuantifierTreeNode):
            return self.bool_quantifier_constraint_builder.evaluate(parameters, expression, self)

        if isinstance(expression, NumQuantifierTreeNode):
            return self.num_quantifier_constraint_builder.evaluate(parameters, expression, self, jml_problem)

        if isinstance(expression, InfixExpression) and hasattr(expression, "left") and hasattr(expression, "right"):
            return self.infix_helper.evaluate_infix(infix_operator=expression.name,
                                                    left=lambda: self.build_expression_constraint(parameters,
                                                                                                  expression.left,
                                                                                                  jml_problem),
                                                    right=lambda: self.build_expression_constraint(parameters,
                                                                                                   expression.right,
                                                                                                   jml_problem),
                                                    is_smt=True,
                                                    get_param=lambda name: parameters[name])

        # TODO: Add question mark expression support

        # TODO: Include all supported expression types
        if isinstance(expression, ArrayIndexNode):
            array = self.build_expression_constraint(parameters, expression.arr_expression, jml_problem)
            expr = self.build_expression_constraint(parameters, expression.index_expression, jml_problem)
            return array[expr]

        if isinstance(expression, ArrayLengthNode):
            arr_name = expression.arr_expr
            if hasattr(arr_name, 'value'):
                array_length_param_key = arr_name.value + "_length"
                array_length_param = parameters[array_length_param_key]
                return array_length_param.value
            else:
                raise Exception("Array length expression not supported")

        # TODO: Add prefix expression support

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
