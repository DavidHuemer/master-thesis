from __future__ import annotations
import nodes.baseNodeRunner
from typing import TypeVar

T = TypeVar('T')


class BaseNodeHandler[T]:
    def __init__(self):
        self.runner: nodes.baseNodeRunner.BaseNodeRunner[T] | None = None
        self.sub_handlers = []

    def is_node(self, t: T):
        """
        Check if the given object is a node
        :param t: The object to check
        :return: True if it is a node, otherwise False
        """
        raise NotImplemented

    def handle(self, t: T):
        """
        Handle the given node
        :param t: The node to handle
        :return: The result of handling the node
        """
        raise NotImplemented

    def evaluate_with_runner(self, t: T, other):
        if not self.runner:
            raise Exception("No runner specified")

        return self.runner.evaluate(t.copy_with_other_node(other))

    def set_runner(self, runner):
        self.runner = runner
        for handler in self.sub_handlers:
            handler.set_runner(runner)
