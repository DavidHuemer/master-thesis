from jpype import JChar, JDouble

from definitions.ast.terminalNode import TerminalNode
from definitions.evaluations.baseExecutinoDto import BaseExecutionDto
from nodes.baseNodeHandler import BaseNodeHandler


class TerminalExecution(BaseNodeHandler[BaseExecutionDto]):

    def is_node(self, t: BaseExecutionDto):
        return isinstance(t.node, TerminalNode)

    def handle(self, t: BaseExecutionDto):
        terminal: TerminalNode = t.node

        if terminal.name == "RESULT":
            return t.result
        elif terminal.name == "INTEGER":
            return int(terminal.value)
        elif terminal.name == "DOUBLE":
            return JDouble(terminal.value)
        elif terminal.name == "IDENTIFIER":
            if t.parameters.parameter_exists(terminal.value):
                return t.parameters.get_parameter_by_key(key=terminal.value,
                                                         use_old=terminal.use_old,
                                                         use_this=terminal.use_this)
            else:
                return None
        elif terminal.name == "BOOL_LITERAL":
            return terminal.value == "true"
        elif terminal.name == "STRING":
            # Return terminal.value without the first and last character (the quotes)
            return terminal.value[1:-1]
        elif terminal.name == "CHAR":
            return JChar(terminal.value[1:-1])
        else:
            return None
