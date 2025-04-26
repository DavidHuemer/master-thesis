from nodes.handlers.BaseArrayIndexNodeHandler import BaseArrayIndexNodeHandler
from verification.resultVerification.resultDto import ResultDto


class ArrayIndexExecution(BaseArrayIndexNodeHandler[ResultDto]):
    def __init__(self):
        super().__init__()
