from definitions import config

from definitions.consistencyTestCase import ConsistencyTestCase
from definitions.verification.verificationResult import VerificationResult
from helper.logs.loggingHelper import LoggingHelper
from pipeline.jmlGenerator.jmlGenerator import JmlGenerator
from pipeline.jmlVerifier.jmlVerifier import JmlVerifier
from verification.result.verificationResultFactory import VerificationResultFactory


class ConsistencyResultGetter:
    def __init__(self, jml_generator=JmlGenerator(), jml_verifier=JmlVerifier()):
        self.jml_generator = jml_generator
        self.jml_verifier = jml_verifier
        self.retries = 0

    def setup(self):
        self.jml_generator.setup()
        self.jml_verifier.setup()

    def get_result(self, consistency_test: ConsistencyTestCase) -> VerificationResult:
        try:
            LoggingHelper.log_info(f"Getting result for {consistency_test.get_name()}")
            self.jml_generator.reset()
            jml_code = self.jml_generator.get_from_test_case(consistency_test)
            return self.get_result_by_jml(consistency_test, jml_code)
        except Exception as e:
            raise e  # Only to reset the retries
        finally:
            self.retries = 0

    def get_result_by_jml(self, consistency_test: ConsistencyTestCase, jml_code: str):
        try:
            LoggingHelper.log_debug("JMl code: \n" + jml_code.strip())
            return self.jml_verifier.verify(consistency_test, jml_code)
        except Exception as e:
            LoggingHelper.log_error(f"Exception occurred: {e}")
            if self.retries >= config.MAX_PIPELINE_TRIES:
                return VerificationResultFactory.by_exception(consistency_test, e)

            LoggingHelper.log_info("Generating new JML")
            # TODO: Get from exception
            new_jml_code = self.jml_generator.get_from_text(str(e))
            self.retries += 1
            return self.get_result_by_jml(consistency_test, new_jml_code)
