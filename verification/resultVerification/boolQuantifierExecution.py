from definitions.ast.quantifier.boolQuantifierTreeNode import BoolQuantifierTreeNode
from definitions.ast.quantifier.boolQuantifierType import BoolQuantifierType
from definitions.codeExecution.result.executionResult import ExecutionResult
from verification.resultVerification.rangeExecution import RangeExecution


class BoolQuantifierExecution:
    def __init__(self, range_execution=RangeExecution()):
        self.range_execution = range_execution

    def evaluate_bool_quantifier(self, result: ExecutionResult, expression: BoolQuantifierTreeNode, result_verifier):
        if expression.quantifier_type == BoolQuantifierType.FORALL:
            return self.evaluate_for_all(result, expression, result_verifier)
        elif expression.quantifier_type == BoolQuantifierType.EXISTS:
            return self.evaluate_exists(result, expression, result_verifier)

        raise Exception("BoolQuantifierExecution: Invalid quantifier type")

    def evaluate_for_all(self, result: ExecutionResult, expression: BoolQuantifierTreeNode, result_verifier):
        for range_result in self.range_execution.execute_range(expression.range_, expression.range_.ranges, result,
                                                               result_verifier):
            evaluation_result = result_verifier.evaluate(range_result, expression.expression)
            if not evaluation_result:
                return False

        return True

    def evaluate_exists(self, result: ExecutionResult, expression: BoolQuantifierTreeNode, result_verifier):
        for range_result in self.range_execution.execute_range(expression.range_, expression.range_.ranges, result,
                                                               result_verifier):
            evaluation_result = result_verifier.evaluate(range_result, expression.expression)
            if evaluation_result:
                return True

        return False
