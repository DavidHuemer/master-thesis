import openai

from ai.Role import Role
from ai.openAIClient import OpenAIClient
from definitions.ai.openAIMessage import OpenAIMessage
from helper.logs.loggingHelper import log_error


class ChatBot:
    """
    Chatbot class that is responsible for chatting with the OpenAI API.
    """

    def __init__(self, client: OpenAIClient = None):
        """
        Initialize the chatbot.
        :param client: The OpenAI client.
        """

        self.client = client or OpenAIClient()
        self.messages: list[OpenAIMessage] = []

    def set_context(self, context: str):
        """
        Set the context of the chatbot.
        :param context: The context.
        """

        if len(self.messages) == 0:
            self.messages.append(OpenAIMessage(Role.SYSTEM, context))
        else:
            self.messages[0] = OpenAIMessage(Role.SYSTEM, context)

    def chat(self, message: str) -> str:
        """
        Chat with the bot.
        :param message: The message to send.
        :return: The response content.
        """

        try:
            self.add_message(Role.USER, message)

            response = self.client.get_response(messages=self.messages)
            response_content = response.choices[0].message.content
            self.add_message(Role.ASSISTANT, response_content)
            return response_content
        except openai.RateLimitError as e:
            if isinstance(e.body, dict):
                raise Exception(e.body['message'] or str(e))
            raise Exception(str(e))
        except Exception as e:
            raise Exception("Error while chatting with the chatbot")

    def add_message(self, role: Role, content: str):
        """
        Add a message to the chat.
        :param role: The role of the message (who sent it).
        :param content: The content of the message.
        """
        self.messages.append(OpenAIMessage(role, content))

    def get_chat(self):
        """
        Get the chat. (The messages in the chat)
        :return: The chat.
        """
        return [message.get_readable() for message in self.messages]

    def reset(self):
        """
        Reset the chat.
        """
        self.messages = [self.messages[0]]
