from definitions.evaluations.tests.testSuite import TestSuite
from definitions.verification.verificationResult import VerificationResult
from helper.logs.loggingHelper import log_info
from util import multiProcessUtil
from verification.testSuite.testSuiteVerificationRunner import run_test_suite_verification


def run_test_suite(test_suite: TestSuite) -> VerificationResult:
    with multiProcessUtil.lock:
        log_info("Running Test Suite")

    return run_test_suite_verification(test_suite)
