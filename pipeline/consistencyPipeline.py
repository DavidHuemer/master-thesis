from codeExecution.vm.VMHelper import VMHelper
from definitions.consistencyTestCase import ConsistencyTestCase
from definitions.verification.verificationResult import VerificationResult
from helper.logs.loggingHelper import LoggingHelper
from pipeline.consistencyResultGetter import ConsistencyResultGetter


class ConsistencyPipeline:
    """
    Class that is responsible for running the pipeline that finds inconsistencies in the java doc.
    """

    def __init__(self, vm_helper=VMHelper(), consistency_result_getter=ConsistencyResultGetter()):
        self.vm_helper = vm_helper
        self.retries = 0
        self.verification_results: list[VerificationResult] = []
        self.consistency_result_getter = consistency_result_getter

    def setup(self):
        LoggingHelper.log_info("Setting up consistency pipeline")
        self.consistency_result_getter.setup()

    def get_results(self, consistency_tests: list[ConsistencyTestCase]) -> list[VerificationResult]:
        try:
            LoggingHelper.log_info("Starting consistency pipeline")
            self.vm_helper.start()
            return [self.consistency_result_getter.get_result(test_case) for test_case in consistency_tests]
        except Exception as e:
            # Only to close the VM even if an exception occurs
            raise e
        finally:
            self.vm_helper.close()
