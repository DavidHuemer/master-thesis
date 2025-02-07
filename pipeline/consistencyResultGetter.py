import os
import time
import traceback

from definitions.consistencyTestCase import ConsistencyTestCase
from definitions.envKeys import MAX_RETRIES, JML_FILE, PARALLEL
from helper.logs.loggingHelper import log_debug, log_error, log_info
from jml.jmlGeneration.jmlProvider import JmlProvider
from jml.jmlGeneration.jmlStorage import store_jml_for_test_case
from pipeline.jmlVerifier.jmlVerifier import verify_jml
from util import multiProcessUtil
from util.Singleton import Singleton
from verification.result.verificationResultFactory import VerificationResultFactory


class ConsistencyResultGetter(Singleton):
    def __init__(self, jml_provider: JmlProvider | None = None):
        self.jml_provider: JmlProvider = jml_provider or JmlProvider()
        self.retries = 0
        self.max_retries = int(os.getenv(MAX_RETRIES))
        self.jml_file_path = os.getenv(JML_FILE)
        self.parallel = os.getenv(PARALLEL) == "true"

    def get_result(self, consistency_test: ConsistencyTestCase):
        try:
            self.jml_provider.reset()
            jml_code = self.jml_provider.get_jml(consistency_test)
            return self.get_result_by_jml(consistency_test, jml_code)
        except Exception as e:
            error = getattr(e, "message", str(e))
            log_error(f"An error occurred when getting a consistency result: {error}")
            return VerificationResultFactory.by_exception(consistency_test, e)
        finally:
            self.retries = 0

    def get_result_by_jml(self, consistency_test: ConsistencyTestCase, jml_code: str):
        try:
            log_debug("JMl code: \n" + jml_code.strip())
            result = verify_jml(consistency_test, jml_code)

            if self.parallel:
                with multiProcessUtil.lock:
                    store_jml_for_test_case(self.jml_file_path, consistency_test, jml_code)
            else:
                store_jml_for_test_case(self.jml_file_path, consistency_test, jml_code)

            return result
        except Exception as e:
            log_error(traceback.format_exc())
            if self.retries >= self.max_retries or not self.jml_provider.fetch_from_server:
                return VerificationResultFactory.by_exception(consistency_test, e)

            log_info("Generating new JML")
            new_jml_code = self.jml_provider.get_by_exception(e)
            self.retries += 1
            return self.get_result_by_jml(consistency_test, new_jml_code)
