from definitions import config
from definitions.consistencyTestCase import ConsistencyTestCase
from definitions.verification.verificationResult import VerificationResult
from helper.logs.loggingHelper import log_info, log_debug, log_error
from jml.jmlGeneration.jmlProvider import JmlProvider
from jml.jmlGeneration.jmlStorage import store_jml_for_test_case
from pipeline.jmlVerifier.jmlVerifier import verify_jml
from util.Singleton import Singleton
from verification.result.verificationResultFactory import VerificationResultFactory


class ConsistencyResultGetter(Singleton):
    def __init__(self, jml_provider: JmlProvider = JmlProvider()):
        self.jml_provider = jml_provider
        self.retries = 0

        # TODO: Add a file that holds the jml codes
        self.path = "jml-results/1.json"

    def get_result(self, consistency_test: ConsistencyTestCase) -> VerificationResult:
        try:
            log_info(f"Getting result for {consistency_test.get_name()}")
            self.jml_provider.reset()
            jml_code = self.jml_provider.get_jml(consistency_test)
            return self.get_result_by_jml(consistency_test, jml_code)
        except Exception as e:
            raise e
        finally:
            self.retries = 0

    def get_result_by_jml(self, consistency_test: ConsistencyTestCase, jml_code: str) -> VerificationResult:
        try:
            log_debug("JMl code: \n" + jml_code.strip())
            result = verify_jml(consistency_test, jml_code)

            if not self.jml_provider.static_jml_exists_for_test_case(consistency_test):
                store_jml_for_test_case(self.path, consistency_test, jml_code)
            return result
        except Exception as e:
            log_error(f"Exception occurred: {e}")
            if self.retries >= config.MAX_PIPELINE_TRIES or self.jml_provider.static_jml_exists():
                return VerificationResultFactory.by_exception(consistency_test, e)

            log_info("Generating new JML")
            new_jml_code = self.jml_provider.jml_generator.get_by_exception(e)
            self.retries += 1
            return self.get_result_by_jml(consistency_test, new_jml_code)
