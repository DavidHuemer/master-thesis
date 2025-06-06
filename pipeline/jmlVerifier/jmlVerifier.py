from definitions.consistencyTestCase import ConsistencyTestCase
from definitions.evaluations.tests.exceptions.noTestCasesException import NoTestCasesException
from testGeneration.testSuiteBuilder import get_test_suite
from verification.result.verificationResultFactory import VerificationResultFactory
from verification.testSuite.testSuiteVerificationRunner import run_test_suite_verification


def verify_jml(consistency_test: ConsistencyTestCase, jml_code: str):
    """
    Verify JML annotations in Java source code.
    """

    test_suite = get_test_suite(consistency_test, jml_code)
    if len(test_suite) <= 0:
        raise NoTestCasesException()

    return run_test_suite_verification(test_suite)
