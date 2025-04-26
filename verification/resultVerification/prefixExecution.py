from nodes.handlers.BasePrefixHandler import BasePrefixHandler
from verification.resultVerification.resultDto import ResultDto


class PrefixExecution(BasePrefixHandler[ResultDto]):
    def __init__(self):
        super().__init__(False)
