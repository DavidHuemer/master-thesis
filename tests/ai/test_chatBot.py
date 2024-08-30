from unittest import TestCase
from unittest.mock import Mock

from ai.chatBot import ChatBot


class TestChatBot(TestCase):
    def setUp(self):
        self.client = Mock()
        self.context = "context"
        self.chatBot = ChatBot(self.client, self.context)

    def test_chat_contains_initial_context(self):
        chat = self.chatBot.get_chat()
        self.assertEqual(len(chat), 1)
        self.assertEqual(f'[system]: {self.context}', chat[0])

    def test_chat_contains_messages(self):
        self.client.get_response.return_value = Mock(choices=[Mock(message=Mock(content="response"))])
        self.chatBot.chat("message")
        chat = self.chatBot.get_chat()
        self.assertEqual(len(chat), 3)
        self.assertEqual(f'[system]: {self.context}', chat[0])
        self.assertEqual(f'[user]: message', chat[1])
        self.assertEqual(f'[assistant]: response', chat[2])
