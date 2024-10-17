from ai.OpenAIClientGenerator import OpenAIClientGenerator
from ai.jmlBot import JmlBot
from ai.openAIClient import OpenAIClient
from definitions.consistencyTestCase import ConsistencyTestCase
from definitions.parser.parserError import ParserError


class JmlAiGenerator:
    """
    Class that is responsible for generating JML using AI.
    """

    def __init__(self, client_generator: OpenAIClientGenerator = OpenAIClientGenerator()):
        self.client_generator = client_generator
        self.client = None
        self.jmlBot: JmlBot | None = None

    def setup(self):
        """
        Sets up the JML AI generator
        :return:
        """
        client = self.client_generator.generate()
        self.client = OpenAIClient(client)
        self.jmlBot = JmlBot(self.client)

    def get_from_test_case(self, test_case: ConsistencyTestCase) -> str:
        """
        Gets JML from a test case
        :param test_case: The test case
        :return: The JML
        """
        return self.jmlBot.get_jml(test_case)

    def get_from_failing_verification(self, parameters):
        return self.jmlBot.get_from_failing_verification(parameters)

    def reset(self):
        if self.jmlBot is not None:
            self.jmlBot.reset()

    def get_from_parser_exception(self, parser_errors: list[ParserError]):
        return self.jmlBot.get_from_parser_exception(parser_errors)

    def get_from_no_test_cases(self):
        return self.jmlBot.get_from_no_test_cases()

    def get_from_text(self, text: str):
        return self.jmlBot.get_from_text(text)
