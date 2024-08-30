from ai.Role import Role
from ai.openAIClient import OpenAIClient
from definitions.ai.openAIMessage import OpenAIMessage


class ChatBot:
    def __init__(self, client: OpenAIClient, context: str):
        """
        Initialize the chatbot.
        :param client: The OpenAI client.
        :param context: The initial context (The description of the chatbot)
        """
        self.client = client
        self.messages: list[OpenAIMessage] = [
            OpenAIMessage(Role.SYSTEM, context)
        ]

    def chat(self, message):
        """
        Chat with the bot.
        :param message: The message to send.
        :return: The response content.
        """
        self.add_message(Role.USER, message)
        response = self.client.get_response(messages=self.messages)
        response_content = response.choices[0].message.content
        self.add_message(Role.ASSISTANT, response_content)
        return response_content

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
