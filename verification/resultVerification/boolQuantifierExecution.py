from definitions.ast.quantifier.boolQuantifierTreeNode import BoolQuantifierTreeNode
from definitions.ast.quantifier.boolQuantifierType import BoolQuantifierType
from nodes.baseNodeHandler import BaseNodeHandler
from verification.resultVerification.rangeExecution import RangeExecution
from verification.resultVerification.resultDto import ResultDto


class BoolQuantifierExecution(BaseNodeHandler[ResultDto]):
    def __init__(self, range_execution=None, quantifier_exec=None):
        super().__init__()
        self.range_execution = range_execution or RangeExecution(quantifier_exec=quantifier_exec)

    def is_node(self, t: ResultDto):
        return isinstance(t.node, BoolQuantifierTreeNode)

    def handle(self, t: ResultDto):
        expression: BoolQuantifierTreeNode = t.node
        if expression.quantifier_type == BoolQuantifierType.FORALL:
            return self.evaluate_for_all(t)
        elif expression.quantifier_type == BoolQuantifierType.EXISTS:
            return self.evaluate_exists(t)

        raise Exception("BoolQuantifierExecution: Invalid quantifier type")

    def evaluate_for_all(self, t: ResultDto):
        expression: BoolQuantifierTreeNode = t.node
        # TODO: Add here all the range variables

        with self.range_execution.execute_range(expression.range_, expression.variable_names, t) as ranges:
            for _ in ranges:
                evaluation_result = self.evaluate_with_runner(t, expression.expression)
                if not evaluation_result:
                    return False

        return True

    def evaluate_exists(self, t: ResultDto):
        expression: BoolQuantifierTreeNode = t.node
        with self.range_execution.execute_range(expression.range_, expression.variable_names, t) as ranges:
            for _ in ranges:
                evaluation_result = self.evaluate_with_runner(t, expression.expression)
                if evaluation_result:
                    return True

        return False
