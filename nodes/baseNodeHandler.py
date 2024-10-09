from typing import TypeVar

T = TypeVar('T')


class BaseNodeHandler[T]:
    def is_node(self, t: T):
        pass

    def handle(self, t: T):
        pass
