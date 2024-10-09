from typing import TypeVar

from nodes.baseNodeHandler import BaseNodeHandler

T = TypeVar('T')


class BaseNodeRunner[T]:
    def __init__(self, terminal_handler: BaseNodeHandler[T],
                 infix_handler: BaseNodeHandler[T],
                 quantifier_handler: BaseNodeHandler[T],
                 question_mark_handler: BaseNodeHandler[T],
                 prefix_handler: BaseNodeHandler[T],
                 array_index_handler: BaseNodeHandler[T],
                 length_handler: BaseNodeHandler[T],
                 reference_handler: BaseNodeHandler[T],
                 method_call_handler: BaseNodeHandler[T]):
        self.terminal_handler = terminal_handler
        self.infix_handler = infix_handler
        self.quantifier_handler = quantifier_handler
        self.question_mark_handler = question_mark_handler
        self.prefix_handler = prefix_handler
        self.array_index_handler = array_index_handler
        self.length_handler = length_handler
        self.reference_handler = reference_handler
        self.method_call_handler = method_call_handler

    def evaluate(self, t: T):
        """
        Evaluate the node
        :return:
        """
        if self.terminal_handler.is_node(t):
            return self.terminal_handler.handle(t)
        elif self.infix_handler.is_node(t):
            return self.infix_handler.handle(t)
        elif self.quantifier_handler.is_node(t):
            return self.quantifier_handler.handle(t)
        elif self.question_mark_handler.is_node(t):
            return self.question_mark_handler.handle(t)
        elif self.prefix_handler.is_node(t):
            return self.prefix_handler.handle(t)
        elif self.array_index_handler.is_node(t):
            return self.array_index_handler.handle(t)
        elif self.length_handler.is_node(t):
            return self.length_handler.handle(t)
        elif self.reference_handler.is_node(t):
            return self.reference_handler.handle(t)
        elif self.method_call_handler.is_node(t):
            return self.method_call_handler.handle(t)

        # TODO: Add additional handlers here, method calls, etc.

        return None
