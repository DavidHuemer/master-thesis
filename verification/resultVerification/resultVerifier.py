from definitions.ast.arrayIndexNode import ArrayIndexNode
from definitions.ast.arrayLengthNode import ArrayLengthNode
from definitions.ast.astTreeNode import AstTreeNode
from definitions.ast.behavior.behaviorNode import BehaviorNode
from definitions.ast.infixExpression import InfixExpression
from definitions.ast.quantifier.boolQuantifierTreeNode import BoolQuantifierTreeNode
from definitions.ast.quantifier.numQuantifierTreeNode import NumQuantifierTreeNode
from definitions.ast.questionMarkNode import QuestionMarkNode
from definitions.ast.terminalNode import TerminalNode
from definitions.codeExecution.result.executionResult import ExecutionResult
from helper.logs.loggingHelper import LoggingHelper
from verification.resultVerification.boolQuantifierExecution import BoolQuantifierExecution
from verification.resultVerification.numQuantifierExecution import NumQuantifierExecution


class ResultVerifier:
    def __init__(self, bool_quantifier_execution=BoolQuantifierExecution(),
                 num_quantifier_execution=NumQuantifierExecution()):
        self.bool_quantifier_execution = bool_quantifier_execution
        self.num_quantifier_execution = num_quantifier_execution

    def verify(self, result: ExecutionResult, behavior_node: BehaviorNode):
        # Run through all post conditions and check if they are satisfied
        for post_condition in behavior_node.post_conditions:
            if not self.evaluate(result, post_condition):
                return False

        return True

    def evaluate(self, result: ExecutionResult, expression: AstTreeNode):
        # Evaluate expression

        if isinstance(expression, QuestionMarkNode):
            expr_result = self.evaluate(result, expression.expr)
            if expr_result:
                return self.evaluate(result, expression.true_expr)
            else:
                return self.evaluate(result, expression.false_expr)

        if isinstance(expression, InfixExpression):
            return self.evaluate_infix(result, expression)

        if isinstance(expression, TerminalNode):
            return self.evaluate_terminal_node(result, expression)

        if isinstance(expression, BoolQuantifierTreeNode):
            return self.bool_quantifier_execution.evaluate_bool_quantifier(result=result, expression=expression,
                                                                           result_verifier=self)

        if isinstance(expression, NumQuantifierTreeNode):
            return self.num_quantifier_execution.evaluate_num_quantifier(result, expression, self)

        if isinstance(expression, ArrayIndexNode):
            index = self.evaluate(result, expression.expression)
            array_name = expression.name
            if array_name in result.parameters:
                array = result.parameters[array_name]
                return array[index]
            else:
                raise Exception(f"Array {array_name} not found in parameters")

        if isinstance(expression, ArrayLengthNode):
            array_name = expression.name
            if array_name in result.parameters:
                array = result.parameters[array_name]
                return len(array)
            else:
                raise Exception(f"Array {array_name} not found in parameters")

        if expression.name == 'negative_number':
            return -self.evaluate(result, expression.children[0])

        for child in expression.children:
            return self.evaluate(result, child)

        return True

    def evaluate_infix(self, result: ExecutionResult, expression: InfixExpression):
        left = self.evaluate(result, expression.left)
        right = self.evaluate(result, expression.right)

        # TODO: Handle all infix operators
        # TODO: Move infix handling to separate class

        if expression.name == "&&":
            return left and right
        elif expression.name == "||":
            return left or right
        elif expression.name == "==":
            return left == right
        elif expression.name == "<==>":
            return left == right
        elif expression.name == "!=":
            return left != right
        elif expression.name == "==>":
            return not left or right
        elif expression.name == "<":
            return left < right
        elif expression.name == "<=":
            return left <= right
        elif expression.name == ">":
            return left > right
        elif expression.name == ">=":
            return left >= right
        elif expression.name == "+":
            return left + right
        elif expression.name == "-":
            return left - right
        elif expression.name == "*":
            return left * right
        else:
            LoggingHelper.log_error(f"Unknown operator {expression.name}")
            return False

    def evaluate_terminal_node(self, result: ExecutionResult, terminal: TerminalNode):
        if terminal.name == "RESULT":
            return result.result
        elif terminal.name == "INTEGER":
            return int(terminal.value)
        elif terminal.name == "IDENTIFIER":
            if terminal.value in result.parameters:
                return result.parameters[terminal.value]
            else:
                return None
        else:
            return None
