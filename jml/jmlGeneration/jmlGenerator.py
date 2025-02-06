from jml.jmlGeneration.jmlAiGenerator import JmlAiGenerator
from definitions.consistencyTestCase import ConsistencyTestCase
from util.Singleton import Singleton


class JmlGenerator(Singleton):
    """
    Class that is responsible for generating JML (Java Modelling Language)
    """

    def __init__(self, jml_ai_generator: JmlAiGenerator | None = None):
        self.jml_ai_generator: JmlAiGenerator = jml_ai_generator or JmlAiGenerator()

    def get_from_test_case(self, test_case: ConsistencyTestCase) -> str:
        return self.jml_ai_generator.get_from_test_case(test_case)

    def setup(self):
        self.jml_ai_generator.setup()

    def reset(self):
        self.jml_ai_generator.reset()

    def get_by_exception(self, e: Exception):
        return self.jml_ai_generator.get_by_exception(e)
