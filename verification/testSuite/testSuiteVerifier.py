from codeExecution.compilation.javaCompilationRunner import JavaCompilationRunner
from definitions.evaluations.tests.testSuite import TestSuite
from definitions.verification.verificationResult import VerificationResult
from definitions.verification.verificatonException import VerificationException
from helper.logs.loggingHelper import LoggingHelper
from verification.result.verificationResultFactory import VerificationResultFactory
from verification.testSuite.testSuiteEnvironmentChecker import TestSuiteEnvironmentChecker
from verification.testSuite.testSuiteVerificationRunner import TestSuiteVerificationRunner


class TestSuiteVerifier:
    def __init__(self, environment_checker=TestSuiteEnvironmentChecker(),
                 java_compilation_runner=JavaCompilationRunner(),
                 test_suite_verification_runner=TestSuiteVerificationRunner()):
        self.environment_checker = environment_checker
        self.java_compilation_runner = java_compilation_runner
        self.test_suite_verification_runner = test_suite_verification_runner

    def run(self, test_suite: TestSuite) -> VerificationResult:
        LoggingHelper.log_info("Running Test Suite")
        # Steps to run the test suite:
        # 1. Check the environment java compiler, ...
        self.environment_checker.check_environment()

        # 2. Compile the Java source code
        self.java_compilation_runner.compile(test_suite.consistency_test_case.java_code)

        # 3. Run the java code and check the results
        return self.test_suite_verification_runner.run(test_suite)
