from definitions import config
from definitions.inconsistencyTestCase import InconsistencyTestCase
from pipeline.jmlGenerator.jmlGenerator import JmlGenerator
from pipeline.jmlVerifier.jmlVerifier import JmlVerifier


class InconsistencyPipeline:
    """
    Class that is responsible for running the pipeline that finds inconsistencies in the java doc.
    """

    def __init__(self, jml_generator=JmlGenerator(), jml_verifier=JmlVerifier()):
        self.jml_generator = jml_generator
        self.jml_verifier = jml_verifier

    def get_results(self, inconsistency_tests: list[InconsistencyTestCase]):
        return [self.get_result(test_case) for test_case in inconsistency_tests]

    def get_result(self, inconsistency_test: InconsistencyTestCase):
        # First, get initial JML
        jml_code = self.jml_generator.get_from_test_case(inconsistency_test)
        result = self.jml_verifier.verify(jml_code)

        if result:
            return result

        for i in range(config.MAX_PIPELINE_TRIES - 1):
            jml_code = self.jml_generator.append_result()
            result = self.jml_verifier.verify(jml_code)
            if result:
                return result

        return False
