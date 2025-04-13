from codeExecution.runtime.codeExecution import execute_on_test_instance
from definitions.codeExecution.result.executionResult import ExecutionResult
from definitions.consistencyTestCase import ConsistencyTestCase
from definitions.verification.testCase import TestCase
from helper.logs.loggingHelper import log_info
from testGeneration.testCaseGeneration.executionExceptionBuilder import build_exception
from testGeneration.testCaseGeneration.javaTypeMapper import get_java_parameters


def execute_method(test_instance, test_case: TestCase, consistency_test_case: ConsistencyTestCase) -> ExecutionResult:
    method_call_parameters = get_java_parameters(test_case, consistency_test_case.method_info.parameters)

    parameters_copy = method_call_parameters.get_original_values().copy()
    try:
        result = execute_on_test_instance(test_instance, parameters=parameters_copy,
                                          consistency_test_case=consistency_test_case)
        exception = None
    except Exception as e:
        log_info(f"Error while executing java method: {e}")
        result = None
        exception = build_exception(e)

    method_call_parameters.update_parameters(parameters_copy)
    return ExecutionResult(result=result, parameters=method_call_parameters, exception=exception)
