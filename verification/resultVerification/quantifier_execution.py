from nodes.baseNodeHandler import BaseNodeHandler
from verification.resultVerification.boolQuantifierExecution import BoolQuantifierExecution
from verification.resultVerification.numQuantifierExecution import NumQuantifierExecution
from verification.resultVerification.resultDto import ResultDto


class QuantifierExecution(BaseNodeHandler[ResultDto]):
    def __init__(self, bool_quantifier_execution=BoolQuantifierExecution(),
                 num_quantifier_execution=NumQuantifierExecution()):
        super().__init__()
        self.bool_quantifier_execution = bool_quantifier_execution
        self.num_quantifier_execution = num_quantifier_execution

    def is_node(self, t: ResultDto):
        return self.bool_quantifier_execution.is_node(t) or self.num_quantifier_execution.is_node(t)

    def handle(self, t: ResultDto):
        if self.bool_quantifier_execution.is_node(t):
            return self.bool_quantifier_execution.handle(t)
        elif self.num_quantifier_execution.is_node(t):
            return self.num_quantifier_execution.handle(t)

        raise Exception("No quantifier found")
