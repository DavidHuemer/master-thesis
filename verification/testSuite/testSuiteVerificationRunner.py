from codeExecution.runtime.javaRuntimeClassLoader import JavaRuntimeClassLoader
from definitions.evaluations.tests.testSuite import TestSuite
from definitions.verification.verificatonException import VerificationException
from verification.behaviors.behaviorsRunner import BehaviorsRunner
from verification.staticVerification.staticMethodVerifier import StaticMethodVerifier
from verification.testCollections.testCollectionsRunner import TestCollectionsRunner


class TestSuiteVerificationRunner:
    """
    Class to run the test suite.
    Must be run inside a VM.
    """

    def __init__(self, runtime_class_loader=JavaRuntimeClassLoader, static_method_verifier=StaticMethodVerifier(),
                 test_collections_runner=TestCollectionsRunner(), behaviors_runner=BehaviorsRunner()):
        self.runtime_class_loader = runtime_class_loader
        self.static_method_verifier = static_method_verifier
        self.test_collections_runner = test_collections_runner
        self.behaviors_runner = behaviors_runner

    def run(self, test_suite: TestSuite):
        # Steps to run the test suite:
        # 1. Get the java class
        test_class = self.runtime_class_loader.get_class(test_suite.get_java())

        # 2. Check if the method exists on the java class
        method_exists = self.static_method_verifier.has_correct_method(test_class, test_suite)
        if not method_exists:
            raise VerificationException("Method does not exist")

        # 3. Run the test cases
        return self.behaviors_runner.run(test_class=test_class, behaviors=test_suite.behavior_tests,
                                         consistency_test_case=test_suite.consistency_test_case)
