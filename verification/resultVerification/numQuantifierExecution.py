from definitions.ast.quantifier.numQuantifierTreeNode import NumQuantifierTreeNode
from definitions.ast.quantifier.numericQuantifierExpressionType import NumericQuantifierExpressionType
from definitions.ast.quantifier.numericQuantifierType import NumericQuantifierType
from nodes.baseNodeHandler import BaseNodeHandler
from verification.resultVerification.rangeExecution import RangeExecution
from verification.resultVerification.resultDto import ResultDto


class NumQuantifierExecution(BaseNodeHandler[ResultDto]):
    def __init__(self, range_execution=None, quantifier_exec=None):
        super().__init__()
        self.range_execution = range_execution or RangeExecution(quantifier_exec=quantifier_exec)

    def is_node(self, t: ResultDto):
        return isinstance(t.node, NumQuantifierTreeNode)

    def handle(self, t: ResultDto):
        expression: NumQuantifierTreeNode = t.node
        return self.evaluate_num_quantifier(expression, t)

    def evaluate_num_quantifier(self, expression: NumQuantifierTreeNode, t: ResultDto):
        if expression.quantifier_expression_type == NumericQuantifierExpressionType.VALUE:
            return self.evaluate_with_value(expression, t)
        elif expression.quantifier_expression_type == NumericQuantifierExpressionType.RANGE:
            return self.evaluate_with_range(expression, t)

        raise Exception("NumQuantifierExecution: Invalid quantifier expression type")

    def evaluate_with_value(self, expression: NumQuantifierTreeNode, t: ResultDto):
        values = [self.evaluate_with_runner(t, expr) for expr in expression.expressions]

        # check if value is a list
        if not isinstance(values, list):
            raise Exception("NumQuantifierExecution: Value is not a list")

        return self.evaluate_list(expression, values)

    def evaluate_list(self, expression: NumQuantifierTreeNode, values: list):
        if expression.quantifier_type == NumericQuantifierType.SUM:
            return sum(values)

        if expression.quantifier_type == NumericQuantifierType.PRODUCT:
            return self.get_product(values)

        if len(values) == 0:
            return None

        if expression.quantifier_type == NumericQuantifierType.MAX:
            return max(values)

        if expression.quantifier_type == NumericQuantifierType.MIN:
            return min(values)

        raise Exception("Numeric quantifier expression type not supported")

    def evaluate_with_range(self, expression: NumQuantifierTreeNode, t: ResultDto):
        values = list(self.get_values_by_range(expression, t))
        return self.evaluate_list(expression, values)

    def get_values_by_range(self, expression: NumQuantifierTreeNode, t: ResultDto):
        with self.range_execution.execute_range(expression.range_, expression.variable_names, t) as ranges:
            for _ in ranges:
                yield self.evaluate_with_runner(t, expression.expressions)

    @staticmethod
    def get_product(value):
        product = 1
        for val in value:
            product *= val

        return product
