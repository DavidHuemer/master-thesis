from definitions.ast.terminalNode import TerminalNode
from definitions.evaluations.baseExecutinoDto import BaseExecutionDto
from helper.terminalHelper import TerminalNodeHandler


class TerminalExecution(TerminalNodeHandler[BaseExecutionDto]):
    def __init__(self):
        super().__init__(False)

    def handle(self, t: BaseExecutionDto):
        terminal: TerminalNode = t.node
        return self.get_original_value(t.node, t.parameters, terminal.use_old, terminal.use_this, t.result)
