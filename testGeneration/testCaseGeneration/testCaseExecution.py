import jpype

from codeExecution.runtime.codeExecution import execute_on_test_instance
from definitions.codeExecution.result.executionResult import ExecutionResult
from definitions.verification.testCase import TestCase
from helper.logs.loggingHelper import log_info
from testGeneration.testCaseGeneration.executionExceptionBuilder import build_exception


def execute_method(test_instance, test_case: TestCase, consistency_test_case) -> ExecutionResult:
    result = get_original_result(test_instance, test_case, consistency_test_case)
    if isinstance(result, ExecutionResult):
        return result

    if isinstance(result, jpype.JArray):
        # noinspection PyTypeChecker
        result = list(result)

    return ExecutionResult(result=result, parameters=test_case.parameters)


def get_original_result(test_instance, test_case, consistency_test_case):
    try:
        return execute_on_test_instance(test_instance, test_case=test_case,
                                        consistency_test_case=consistency_test_case)
    except Exception as e:
        log_info(f"Error while executing java method: {e}")
        exception = build_exception(e)
        return ExecutionResult(result=None, parameters=test_case.parameters, exception=exception)
