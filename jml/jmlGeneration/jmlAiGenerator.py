from definitions.consistencyTestCase import ConsistencyTestCase
from jml.jmlGeneration.jmlBot import JmlBot


class JmlAiGenerator:
    """
    Class that is responsible for generating JML using AI.
    """

    def __init__(self, jml_bot: JmlBot):
        self.jml_bot = jml_bot

    def get_from_test_case(self, test_case: ConsistencyTestCase) -> str:
        """
        Gets JML from a test case
        :param test_case: The test case
        :return: The JML
        """
        return self.jml_bot.get_jml(test_case)

    def reset(self):
        if self.jml_bot is not None:
            self.jml_bot.reset()

    def get_by_exception(self, e: Exception):
        return self.jml_bot.get_from_exception(e)
