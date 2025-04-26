from definitions.ast.astTreeNode import AstTreeNode


class BaseDto:
    """
    Base DTO that is used for node evaluations
    """

    def __init__(self, node: AstTreeNode):
        """
        Constructor for the BaseDto
        :param node: The node to evaluate
        """
        self.node = node

    def copy_with_other_node(self, node):
        """
        Copies the whole DTO with another node
        :param node: The node to copy with
        :return: The copied DTO
        """
        raise NotImplementedError("Copy with other node not implemented")
