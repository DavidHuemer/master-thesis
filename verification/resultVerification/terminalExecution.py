from jpype import JChar, JDouble, JString, JInt, JBoolean

from definitions.ast.terminalNode import TerminalNode
from definitions.evaluations.baseExecutinoDto import BaseExecutionDto
from nodes.baseNodeHandler import BaseNodeHandler


class TerminalExecution(BaseNodeHandler[BaseExecutionDto]):

    def is_node(self, t: BaseExecutionDto):
        return isinstance(t.node, TerminalNode)

    def handle(self, t: BaseExecutionDto):
        original = self.get_original_value(t)

        if isinstance(original, str):
            return JString(original)
        elif isinstance(original, int):
            return JInt(original)
        elif isinstance(original, float):
            return JDouble(original)
        elif isinstance(original, bool):
            return JBoolean(original)

        return original

    def get_original_value(self, t: BaseExecutionDto):
        terminal: TerminalNode = t.node

        if terminal.name == "RESULT":
            return t.result
        elif terminal.name == "INTEGER":
            return JInt(terminal.value)
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
            return JBoolean(terminal.value == "true")
        elif terminal.name == "STRING":
            # Return terminal.value without the first and last character (the quotes)
            return JString(terminal.value[1:-1])
        elif terminal.name == "CHAR":
            return JChar(terminal.value[1:-1])
        else:
            return None
