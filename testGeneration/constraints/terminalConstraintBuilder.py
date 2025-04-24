from typing import cast

from definitions.ast.terminalNode import TerminalNode
from helper.terminalHelper import TerminalNodeHandler
from testGeneration.constraints.constraintsDto import ConstraintsDto


class TerminalConstraintBuilder(TerminalNodeHandler[ConstraintsDto]):
    def __init__(self):
        super().__init__(True)

    def handle(self, t: ConstraintsDto):
        return self.get_value(cast(TerminalNode, t.node), t.constraint_parameters)
