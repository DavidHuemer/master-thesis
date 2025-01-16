import jpype

from codeExecution.runtime.codeExecution import CodeExecution
from definitions.codeExecution.result.executionResult import ExecutionResult
from definitions.verification.testCase import TestCase
from helper.logs.loggingHelper import log_info
from testGeneration.testCaseGeneration.executionExceptionBuilder import ExecutionExceptionBuilder


class TestCaseExecution:
    def __init__(self, code_execution=CodeExecution(),
                 execution_exception_builder=ExecutionExceptionBuilder()):
        self.code_execution = code_execution
        self.execution_exception_builder = execution_exception_builder

    def execute_method(self, test_instance, test_case: TestCase, consistency_test_case) -> ExecutionResult:
        result = self.get_original_result(test_instance, test_case, consistency_test_case)
        if isinstance(result, ExecutionResult):
            return result

        if isinstance(result, jpype.JArray):
            # noinspection PyTypeChecker
            result = list(result)

        return ExecutionResult(result=result, parameters=test_case.parameters)

    def get_original_result(self, test_instance, test_case, consistency_test_case):
        try:
            return self.code_execution.execute(test_instance, test_case=test_case,
                                               consistency_test_case=consistency_test_case)
        except Exception as e:
            log_info(f"Error while executing java method: {e}")
            exception = self.execution_exception_builder.build_exception(e)
            return ExecutionResult(result=None, parameters=test_case.parameters, exception=exception)
