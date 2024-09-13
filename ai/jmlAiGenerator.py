from ai.OpenAIClientGenerator import OpenAIClientGenerator
from ai.jmlBot import JmlBot
from ai.openAIClient import OpenAIClient
from definitions.inconsistencyTestCase import InconsistencyTestCase


class JmlAiGenerator:
    """
    Class that is responsible for generating JML using AI.
    """

    def __init__(self, client_generator: OpenAIClientGenerator = OpenAIClientGenerator()):
        self.client_generator = client_generator
        self.client = None
        self.jmlBot = None

    def setup(self):
        """
        Sets up the JML AI generator
        :return:
        """
        client = self.client_generator.generate()
        self.client = OpenAIClient(client)
        self.jmlBot = JmlBot(self.client)

    def get_from_test_case(self, test_case: InconsistencyTestCase) -> str:
        """
        Gets JML from a test case
        :param test_case: The test case
        :return: The JML
        """
        return self.jmlBot.get_jml(test_case)
