from codeExecution.duplication.javaDuplicationHelper import JavaDuplicationHelper
from codeExecution.runtime.javaClassInstantiation import JavaClassInstantiation
from definitions.ast.behavior.behaviorNode import BehaviorNode
from definitions.codeExecution.runtime.javaRuntimeClass import JavaRuntimeClass
from definitions.consistencyTestCase import ConsistencyTestCase
from definitions.verification.testCase import TestCase
from verification.resultVerification.executionVerifier import ExecutionVerifier
from verification.testCase.testCaseExecution import TestCaseExecution


class TestCaseRunner:
    def __init__(self, java_class_instantiation=JavaClassInstantiation(),
                 java_duplication_helper=JavaDuplicationHelper(),
                 test_case_execution=TestCaseExecution(),
                 execution_verifier=ExecutionVerifier()):
        self.java_class_instantiation = java_class_instantiation
        self.java_duplication_helper = java_duplication_helper
        self.test_case_execution = test_case_execution
        self.execution_verifier = execution_verifier

    # TODO: Return more than just a boolean (e.g. why the test failed)
    def run(self, test_class: JavaRuntimeClass,
            test_case: TestCase, consistency_test_case: ConsistencyTestCase,
            behavior: BehaviorNode, expected_exception=None) -> bool:
        # Steps to run a test case:
        # 1. Get instance of the testing class
        test_instance = self.java_class_instantiation.instantiate(test_class)

        # 2. Get the current parameters list of the class instance before the execution
        # TODO: Get the current parameters list of the class instance before the execution
        old_duplicate = self.java_duplication_helper.duplicate(test_class, test_instance)

        # 3. execute the method with the parameters
        execution_result = self.test_case_execution.execute_method(test_instance, test_case, consistency_test_case)

        return self.execution_verifier.verify(execution_result=execution_result,
                                              behavior=behavior,
                                              expected_exception=expected_exception,
                                              consistency_test_case=consistency_test_case,
                                              test_case=test_case)
