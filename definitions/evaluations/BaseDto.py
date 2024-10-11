from nodes.baseNodeRunner import BaseNodeRunner


class BaseDto:
    """
    Base DTO that is used for node evaluations
    """

    def __init__(self, node, runner: BaseNodeRunner):
        """
        Constructor for the BaseDto
        :param node: The node to evaluate
        """
        self.node = node
        self.runner = runner

    def copy_with_other_node(self, node):
        """
        Copies the whole DTO with another node
        :param node: The node to copy with
        :return: The copied DTO
        """
        raise NotImplementedError("Copy with other node not implemented")

    def evaluate_with_other_node(self, node):
        """
        Evaluate the given node with the values of the DTO
        :param node: The node to evaluate
        :return: The evaluated node
        """
        return self.runner.evaluate(self.copy_with_other_node(node))
