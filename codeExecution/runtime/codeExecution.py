import jpype
from codetiming import Timer

from definitions.consistencyTestCase import ConsistencyTestCase
from definitions.evaluations.csp.parameters.methodCallParameters import MethodCallParameters
from definitions.verification.testCase import TestCase

code_execution_timer = Timer(name="code_execution", logger=None)


def execute_on_test_instance(test_instance, parameters: list,
                             consistency_test_case: ConsistencyTestCase):
    method_to_call = getattr(test_instance, consistency_test_case.method_info.name)
    return execute_with_parameters(method_to_call, parameters)


@code_execution_timer
def execute_with_parameters(method_to_call, parameters_list: list[jpype.JObject]):
    return method_to_call(*parameters_list)
