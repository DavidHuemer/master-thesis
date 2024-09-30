from definitions.ast.quantifier.numQuantifierTreeNode import NumQuantifierTreeNode
from definitions.ast.quantifier.numericQuantifierExpressionType import NumericQuantifierExpressionType
from definitions.ast.quantifier.numericQuantifierType import NumericQuantifierType
from definitions.codeExecution.result.executionResult import ExecutionResult
from verification.resultVerification.rangeExecution import RangeExecution


class NumQuantifierExecution:
    def __init__(self, range_execution=RangeExecution()):
        self.range_execution = range_execution

    def evaluate_num_quantifier(self, result: ExecutionResult, expression: NumQuantifierTreeNode, result_verifier):
        if expression.quantifier_expression_type == NumericQuantifierExpressionType.VALUE:
            return self.evaluate_with_value(result, expression, result_verifier)
        elif expression.quantifier_expression_type == NumericQuantifierExpressionType.RANGE:
            return self.evaluate_with_range(result, expression, result_verifier)

        raise Exception("NumQuantifierExecution: Invalid quantifier expression type")

    def evaluate_with_value(self, result: ExecutionResult, expression: NumQuantifierTreeNode, result_verifier):
        values = [result_verifier.evaluate(result, expr) for expr in expression.expressions]

        # check if value is a list
        if not isinstance(values, list):
            raise Exception("NumQuantifierExecution: Value is not a list")

        return self.evaluate_list(expression, values)

    def evaluate_list(self, expression: NumQuantifierTreeNode, values: list):
        if len(values) == 0:
            return None

        if expression.quantifier_type == NumericQuantifierType.MAX:
            return max(values)

        if expression.quantifier_type == NumericQuantifierType.MIN:
            return min(values)

        if expression.quantifier_type == NumericQuantifierType.SUM:
            return sum(values)

        if expression.quantifier_type == NumericQuantifierType.PRODUCT:
            return self.get_product(values)

        raise Exception("Numeric quantifier expression type not supported")

    def evaluate_with_range(self, result: ExecutionResult, expression: NumQuantifierTreeNode, result_verifier):
        values = list(self.get_values_by_range(result, expression, result_verifier))
        return self.evaluate_list(expression, values)

    def get_values_by_range(self, result: ExecutionResult, expression: NumQuantifierTreeNode, result_verifier):
        r = self.range_execution.execute_range(expression.range_, expression.range_.ranges, result,
                                               result_verifier)

        for range_result in r:
            yield result_verifier.evaluate(range_result, expression.expressions)

    @staticmethod
    def get_product(value):
        product = 1
        for val in value:
            product *= val

        return product
