from typing import TypeVar

T = TypeVar('T')


class BaseNodeHandler[T]:
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
