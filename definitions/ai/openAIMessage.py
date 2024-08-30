from ai.Role import Role


class OpenAIMessage:
    """
    Represents a message of the OpenAI chat API.
    """

    def __init__(self, role: Role, content: str):
        """
        Initialize the message.

        :param role: The role of the message.
        :param content: The content of the message.
        """
        self.role = role
        self.content = content

    def get_json(self):
        """
        Get the JSON representation of the message.

        :return: The JSON representation of the message.
        """
        return {
            "role": self.role.value,
            "content": self.content,
        }

    def get_readable(self):
        """
        Get the readable representation of the message.

        :return: The readable representation of the message.
        """
        return f'[{self.role.value}]: {self.content}'
