from codeExecution.runtime.codeExecution import execute_on_test_instance
from definitions.codeExecution.result.executionResult import ExecutionResult
from definitions.consistencyTestCase import ConsistencyTestCase
from definitions.parameters.Variables import Variables
from helper.logs.loggingHelper import log_info
from helper.parameterHelper.parameterValueGenerator import get_parameter_value_by_java
from testGeneration.testCaseGeneration.executionExceptionBuilder import build_exception


def execute_method(test_instance, variables: Variables, consistency_test_case: ConsistencyTestCase) -> ExecutionResult:
    method_call_parameters = variables.method_call_parameters

    method_call_dict = {parameter.name: parameter.get_state().parameter_value.java_value
                        for parameter in method_call_parameters.get_parameter_list()}

    method_call_dict_copy = method_call_dict.copy()
    real_parameters = list(method_call_dict_copy.values())
    exception = None
    try:
        result = execute_on_test_instance(test_instance, parameters=real_parameters,
                                          consistency_test_case=consistency_test_case)
    except Exception as e:
        log_info(f"Error while executing java method: {e}")
        result = None
        exception = build_exception(e)

    for key in method_call_dict:
        new_value = get_parameter_value_by_java(method_call_dict_copy[key])
        method_call_parameters[key].update_new(new_value)

    return ExecutionResult(result=result, parameters=method_call_parameters, exception=exception)

    # method_call_parameters = get_java_parameters(test_case, consistency_test_case.method_info.parameters)
    #
    #
    #
    #
    #
    # parameters_copy = method_call_parameters.get_original_values().copy()
    # try:
    #     result = execute_on_test_instance(test_instance, parameters=parameters_copy,
    #                                       consistency_test_case=consistency_test_case)
    #     exception = None
    # except Exception as e:
    #     log_info(f"Error while executing java method: {e}")
    #     result = None
    #     exception = build_exception(e)
    #
    # method_call_parameters.update_parameters(parameters_copy)
    # return ExecutionResult(result=result, parameters=method_call_parameters, exception=exception)
