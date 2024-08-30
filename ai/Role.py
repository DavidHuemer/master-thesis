from enum import Enum


class Role(Enum):
    """
    Define the role of a message in a conversation.
    """
    SYSTEM = 'system'
    USER = 'user'
    ASSISTANT = 'assistant'
