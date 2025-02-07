import jpype

from codeExecution.runtime.codeExecution import execute_on_test_instance
from definitions.codeExecution.result.executionResult import ExecutionResult
from definitions.evaluations.csp.parameters.methodCallParameters import MethodCallParameters
from definitions.verification.testCase import TestCase
from helper.logs.loggingHelper import log_info
from testGeneration.testCaseGeneration.executionExceptionBuilder import build_exception


def execute_method(test_instance, test_case: TestCase, consistency_test_case) -> ExecutionResult:
    parameters_copy = MethodCallParameters()
    for key in test_case.parameters.parameters:
        value = test_case.parameters.parameters[key]

        if isinstance(value, list):
            parameters_copy[key] = jpype.JArray(jpype.JInt, 1)(value)
        else:
            parameters_copy[key] = value

    # Update the parameters the following way: if a param is a list, replace it with JArray

    result = get_original_result(test_instance, test_case.parameters, parameters_copy, consistency_test_case)
    if isinstance(result, ExecutionResult):
        return result

    if isinstance(result, jpype.JArray):
        # noinspection PyTypeChecker
        result = list(result)

    return ExecutionResult(result=result, parameters=parameters_copy)


def get_original_result(test_instance, original_method_call_params: MethodCallParameters,
                        parameters: MethodCallParameters,
                        consistency_test_case):
    try:
        return execute_on_test_instance(test_instance, parameters=parameters,
                                        consistency_test_case=consistency_test_case)
    except Exception as e:
        log_info(f"Error while executing java method: {e}")
        exception = build_exception(e)
        return ExecutionResult(result=None, parameters=original_method_call_params, exception=exception)
