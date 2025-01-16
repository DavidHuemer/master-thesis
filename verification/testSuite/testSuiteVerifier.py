import time

from codetiming import Timer

from definitions.evaluations.tests.testSuite import TestSuite
from definitions.verification.verificationResult import VerificationResult
from helper.logs.loggingHelper import log_info
from verification.testSuite.testSuiteVerificationRunner import run_test_suite_verification

test_suite_run_timer = Timer(name="run_test_suite", text="Running test suite")


@test_suite_run_timer
def run_test_suite(test_suite: TestSuite) -> VerificationResult:
    log_info("Running Test Suite")
    result = run_test_suite_verification(test_suite)
    return result
