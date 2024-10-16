from definitions.consistencyTestCase import ConsistencyTestCase
from definitions.evaluations.tests.exceptions.noTestCasesException import NoTestCasesException
from definitions.verification.verificationResult import VerificationResult
from helper.logs.loggingHelper import LoggingHelper
from verification.testSuite.testSuiteBuilder import TestSuiteBuilder
from verification.testSuite.testSuiteVerifier import TestSuiteVerifier


class JmlVerifier:
    """
    Class to verify JML annotations in Java source code.
    """

    def __init__(self, test_suite_builder=TestSuiteBuilder(), test_suite_verifier=TestSuiteVerifier()):
        self.test_suite_builder = test_suite_builder
        self.test_suite_verifier = test_suite_verifier

    def setup(self):
        self.test_suite_verifier.setup()

    def verify(self, test_case: ConsistencyTestCase, jml_code: str) -> VerificationResult:
        """
        Verify JML annotations in Java source code.
        """
        LoggingHelper.log_info("Starting JML Verification")

        # Steps:
        # 1. Get the test cases (different parameters for the testing method)
        test_suite = self.test_suite_builder.get_test_suite(test_case, test_case.method_info, jml_code)
        LoggingHelper.log_info("Test Suite created")

        if test_suite.get_test_cases_count() <= 0:
            raise NoTestCasesException()

        # 2. Run the test cases (Run the method with the different parameters)
        return self.test_suite_verifier.run(test_suite)
