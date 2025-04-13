from nodes.baseNodeHandler import BaseNodeHandler
from verification.resultVerification.boolQuantifierExecution import BoolQuantifierExecution
from verification.resultVerification.numQuantifierExecution import NumQuantifierExecution
from verification.resultVerification.resultDto import ResultDto


class QuantifierExecution(BaseNodeHandler[ResultDto]):
    def __init__(self, bool_quantifier_execution=None,
                 num_quantifier_execution=None):
        super().__init__()
        self.bool_quantifier_execution = bool_quantifier_execution or BoolQuantifierExecution()
        self.num_quantifier_execution = num_quantifier_execution or NumQuantifierExecution()

    def set_runner(self, runner):
        super().set_runner(runner)
        self.bool_quantifier_execution.set_runner(runner)
        self.num_quantifier_execution.set_runner(runner)

    def is_node(self, t: ResultDto):
        return self.bool_quantifier_execution.is_node(t) or self.num_quantifier_execution.is_node(t)

    def handle(self, t: ResultDto):
        if self.bool_quantifier_execution.is_node(t):
            return self.bool_quantifier_execution.handle(t)
        elif self.num_quantifier_execution.is_node(t):
            return self.num_quantifier_execution.handle(t)

        raise Exception("No quantifier found")
