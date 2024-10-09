from definitions.ast.terminalNode import TerminalNode
from nodes.baseNodeHandler import BaseNodeHandler
from verification.resultVerification.resultDto import ResultDto


class TerminalExecution(BaseNodeHandler[ResultDto]):

    def is_node(self, t: ResultDto):
        return isinstance(t.node, TerminalNode)

    def handle(self, t: ResultDto):
        terminal: TerminalNode = t.node

        if terminal.name == "RESULT":
            return t.result
        elif terminal.name == "INTEGER":
            return int(terminal.value)
        elif terminal.name == "IDENTIFIER":
            if t.result_parameters.parameter_exists(terminal.value):
                return t.result_parameters.get_parameter_by_key(key=terminal.value,
                                                                use_old=terminal.use_old,
                                                                use_this=terminal.use_this)
            else:
                return None
        elif terminal.name == "BOOL_LITERAL":
            return terminal.value == "true"
        else:
            return None
