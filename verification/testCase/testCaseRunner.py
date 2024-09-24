from codeExecution.duplication.javaDuplicationHelper import JavaDuplicationHelper
from codeExecution.runtime.codeExecution import CodeExecution
from codeExecution.runtime.javaClassInstantiation import JavaClassInstantiation
from definitions.ast.behavior.behaviorNode import BehaviorNode
from definitions.codeExecution.result.executionResult import ExecutionResult
from definitions.codeExecution.runtime.javaRuntimeClass import JavaRuntimeClass
from definitions.consistencyTestCase import ConsistencyTestCase
from definitions.verification.testCase import TestCase
from helper.logs.loggingHelper import LoggingHelper
from verification.resultVerification.resultVerifier import ResultVerifier


class TestCaseRunner:
    def __init__(self, java_class_instantiation=JavaClassInstantiation(),
                 java_duplication_helper=JavaDuplicationHelper(),
                 code_execution=CodeExecution(),
                 result_verifier=ResultVerifier()):
        self.java_class_instantiation = java_class_instantiation
        self.java_duplication_helper = java_duplication_helper
        self.code_execution = code_execution
        self.result_verifier = result_verifier

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
        execution_result = self.execute_method(test_instance, test_case, consistency_test_case)
        if expected_exception is not None:
            return expected_exception in execution_result.exception

        if execution_result.exception is not None:
            return False

        # 4. Get the current parameters list of the class instance after the execution
        # TODO: Get the current parameters list of the class instance after the execution

        verification_result = self.result_verifier.verify(execution_result, behavior)

        LoggingHelper.log_debug(f'Verified {consistency_test_case.method_info.name} with {test_case.parameters}. '
                                f'Result: {execution_result.result}.'
                                f'Consistency result: {verification_result}')

        return verification_result

    def execute_method(self, test_instance, test_case, consistency_test_case):
        try:
            execution_result = self.code_execution.execute(test_instance, test_case=test_case,
                                                           consistency_test_case=consistency_test_case)

            return ExecutionResult(result=execution_result, parameters=test_case.parameters)
        except Exception as e:
            name = e.getClass().getName()
            return ExecutionResult(result=None, parameters=test_case.parameters, exception=name)
