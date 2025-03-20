from jpype import JChar

from definitions.ast.terminalNode import TerminalNode
from definitions.evaluations.baseExecutinoDto import BaseExecutionDto
from helper.terminalHelper import TerminalNodeHandler
from verification.resultVerification.jpypeValueTransformation import transform_to_jpype_value


class TerminalExecution(TerminalNodeHandler[BaseExecutionDto]):
    def __init__(self):
        super().__init__(False)

    def handle(self, t: BaseExecutionDto):
        terminal: TerminalNode = t.node
        original = self.get_original_value(t.node, t.parameters, terminal.use_old, terminal.use_this, t.result)
        if terminal.name == "CHAR":
            original = JChar(original)
        return transform_to_jpype_value(original)
