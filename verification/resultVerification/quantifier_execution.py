from nodes.BaseSubNodeHandler import BaseSubNodeHandler
from verification.resultVerification.boolQuantifierExecution import BoolQuantifierExecution
from verification.resultVerification.numQuantifierExecution import NumQuantifierExecution
from verification.resultVerification.resultDto import ResultDto


class QuantifierExecution(BaseSubNodeHandler[ResultDto]):
    def __init__(self, bool_quantifier_execution=None,
                 num_quantifier_execution=None):
        super().__init__()
        self.bool_quantifier_execution = bool_quantifier_execution or BoolQuantifierExecution()
        self.num_quantifier_execution = num_quantifier_execution or NumQuantifierExecution()

        self.sub_handlers = [self.bool_quantifier_execution, self.num_quantifier_execution]
