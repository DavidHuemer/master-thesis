from unittest import TestCase
from unittest.mock import Mock

from parameterized import parameterized

from jml.jmlGeneration.jmlBot import JmlBot
from definitions.parser.parserError import ParserError
from definitions.parser.parserException import ParserException


class TestJmlBot(TestCase):
    def setUp(self):
        self.client = Mock()
        self.chat_bot = Mock()
        self.ai_template_generator = Mock()
        self.jml_bot = JmlBot(self.client, self.chat_bot, ai_template_generator=self.ai_template_generator)

    @parameterized.expand([
        (Exception("Test"), "Test"),
        (Exception("Test1"), "Test1"),
        (ParserException([]), "Parser exception occurred"),
        (ParserException([ParserError(1, 2, "lexer")]), "Parser exception occurred:\nLine 1:2 - lexer"),
    ])
    def test_get_from_exception(self, exception: Exception, expected: str):
        self.chat_bot.chat.return_value = "Test"
        self.jml_bot.get_from_exception(exception)

        # Assert that the ai_template_generator.generate_by_exception method was called with the correct argument
        self.ai_template_generator.generate_by_exception.assert_called_with(expected)
