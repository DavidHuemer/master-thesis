from ai.jmlAiGenerator import JmlAiGenerator
from definitions.consistencyTestCase import ConsistencyTestCase
from definitions.parser.parserException import ParserException
from definitions.verification.verificationResult import VerificationResult


class JmlGenerator:
    """
    Class that is responsible for generating JML (Java Modelling Language)
    """

    def __init__(self, jml_ai_generator=JmlAiGenerator()):
        self.jml_ai_generator = jml_ai_generator

    def get_from_test_case(self, test_case: ConsistencyTestCase) -> str:
        return self.jml_ai_generator.get_from_test_case(test_case)

    def setup(self):
        self.jml_ai_generator.setup()

    def reset(self):
        self.jml_ai_generator.reset()

    def get_from_parser_exception(self, inconsistency_test, parser_exception: ParserException):
        return self.jml_ai_generator.get_from_parser_exception(node=parser_exception.error_node)

    def get_from_failing_verification(self, result: VerificationResult):
        return self.jml_ai_generator.get_from_failing_verification(result.parameters)

    def get_from_no_test_cases(self):
        return self.jml_ai_generator.get_from_no_test_cases()

    def get_from_text(self, text: str):
        return self.jml_ai_generator.get_from_text(text)
