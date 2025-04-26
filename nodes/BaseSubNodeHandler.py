from nodes.baseNodeHandler import BaseNodeHandler


class BaseSubNodeHandler[T](BaseNodeHandler[T]):
    def __init__(self):
        super().__init__()
        self.sub_handlers: list[BaseNodeHandler[T]] = []

    def is_node(self, t: T):
        return any([handler.is_node(t) for handler in self.sub_handlers])

    def handle(self, t: T):
        for handler in self.sub_handlers:
            if handler.is_node(t):
                return handler.handle(t)

    def set_runner(self, runner):
        super().set_runner(runner)
        for handler in self.sub_handlers:
            handler.set_runner(runner)
