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
                 method_call_handler: BaseNodeHandler[T]):

        self.handlers: list[BaseNodeHandler[T]] = []

        handlers = locals()
        for name, handler in handlers.items():
            if isinstance(handler, BaseNodeHandler):
                handler.set_runner(self)
                self.handlers.append(handler)

    def evaluate(self, t: T):
        """
        Evaluate the node
        :return:
        """

        for handler in self.handlers:
            if handler.is_node(t):
                return handler.handle(t)

        return None
