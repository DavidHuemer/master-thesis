from codeExecution.runtime.javaRuntimeClassLoader import get_class
from definitions.evaluations.tests.testSuite import TestSuite
from definitions.verification.verificatonException import VerificationException
from verification.behaviors.behaviorsRunner import run_behaviors
from verification.staticVerification.staticMethodVerifier import has_correct_method


def run_test_suite_verification(test_suite: TestSuite):
    # Steps to run the test suite:
    # 1. Get the java class
    test_class = get_class(test_suite.get_java())

    # 2. Check if the method exists on the java class
    method_exists = has_correct_method(test_class, test_suite)
    if not method_exists:
        raise VerificationException("Method does not exist")

    # 3. Run the test cases
    return run_behaviors(test_class=test_class, behaviors=test_suite.behavior_tests,
                         consistency_test_case=test_suite.consistency_test_case)
