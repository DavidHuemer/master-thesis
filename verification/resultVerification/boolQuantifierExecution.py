from definitions.ast.quantifier.boolQuantifierTreeNode import BoolQuantifierTreeNode
from definitions.ast.quantifier.boolQuantifierType import BoolQuantifierType
from nodes.baseNodeHandler import BaseNodeHandler
from verification.resultVerification.rangeExecution import RangeExecution
from verification.resultVerification.resultDto import ResultDto


class BoolQuantifierExecution(BaseNodeHandler[ResultDto]):
    def __init__(self, range_execution=RangeExecution()):
        super().__init__()
        self.range_execution = range_execution

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

        for _ in self.range_execution.execute_range(expression.range_, expression.variable_names, t):
            evaluation_result = self.evaluate_with_runner(t, expression.expression)
            if not evaluation_result:
                for var_name in expression.variable_names:
                    t.get_result_parameters().local_parameters.pop(var_name[1])
                return False

        # TODO: Remove here all the range variables of the current range
        for var_name in expression.variable_names:
            t.get_result_parameters().local_parameters.pop(var_name[1])

        return True

    def evaluate_exists(self, t: ResultDto):
        expression: BoolQuantifierTreeNode = t.node
        for _ in self.range_execution.execute_range(expression.range_, expression.variable_names, t):
            evaluation_result = self.evaluate_with_runner(t, expression.expression)
            if evaluation_result:
                return True

        for var_name in expression.variable_names:
            t.get_result_parameters().local_parameters.pop(var_name[1])
        return False
