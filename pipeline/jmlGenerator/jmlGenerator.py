from ai.jmlAiGenerator import JmlAiGenerator
from definitions.inconsistencyTestCase import InconsistencyTestCase


class JmlGenerator:
    """
    Class that is responsible for generating JML (Java Modelling Language)
    """

    def __init__(self, jml_ai_generator=JmlAiGenerator()):
        self.jml_ai_generator = jml_ai_generator

    def get_from_test_case(self, test_case: InconsistencyTestCase) -> str:
        return self.jml_ai_generator.get_from_test_case(test_case)

    def setup(self):
        self.jml_ai_generator.setup()
