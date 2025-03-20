from definitions.consistencyTestCase import ConsistencyTestCase
from jml.jmlGeneration.jmlBot import JmlBot
from util.Singleton import Singleton


class JmlGenerator(Singleton):
    """
    Class that is responsible for generating JML (Java Modelling Language)
    """

    def __init__(self, jml_bot: JmlBot | None = None):
        self.jml_bot: JmlBot = jml_bot or JmlBot()

    def get_from_test_case(self, test_case: ConsistencyTestCase) -> str:
        return self.jml_bot.get_jml(test_case)

    def setup(self):
        self.jml_bot.setup()

    def reset(self):
        self.jml_bot.reset()

    def get_by_exception(self, e: Exception):
        return self.jml_bot.get_from_exception(e)
