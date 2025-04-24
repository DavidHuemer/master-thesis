from typing import cast

from definitions.ast.terminalNode import TerminalNode
from definitions.evaluations.baseExecutinoDto import BaseExecutionDto
from helper.terminalHelper import TerminalNodeHandler


class TerminalExecution(TerminalNodeHandler[BaseExecutionDto]):
    def __init__(self):
        super().__init__(False)

    def handle(self, t: BaseExecutionDto):
        return self.get_value(cast(TerminalNode, t.node), t.parameters, t.result)
