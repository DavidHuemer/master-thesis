from codetiming import Timer

from definitions.consistencyTestCase import ConsistencyTestCase
from definitions.evaluations.tests.exceptions.noTestCasesException import NoTestCasesException
from helper.logs.loggingHelper import log_info
from testGeneration.testSuiteBuilder import get_test_suite
from verification.testSuite.testSuiteVerifier import run_test_suite

verify_jml_timer = Timer(name="verify_jml", logger=None)


@verify_jml_timer
def verify_jml(consistency_test: ConsistencyTestCase, jml_code: str):
    """
    Verify JML annotations in Java source code.
    """
    log_info("Starting JML Verification")

    # 1. Get the test suite
    test_suite = get_test_suite(consistency_test, jml_code)
    log_info("Test Suite created")

    if len(test_suite) <= 0:
        raise NoTestCasesException()

    return run_test_suite(test_suite)
