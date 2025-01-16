from codetiming import Timer

from definitions.consistencyTestCase import ConsistencyTestCase
from definitions.verification.testCase import TestCase

code_execution_timer = Timer(name="code_execution", logger=None)


class CodeExecution:
    @staticmethod
    def execute(test_instance, test_case: TestCase, consistency_test_case: ConsistencyTestCase):
        method_to_call = getattr(test_instance, consistency_test_case.method_info.name)
        parameters = test_case.parameters
        parameters_list = list(parameters.parameters.values())
        return CodeExecution.execute_with_parameters(method_to_call, parameters_list)

    @staticmethod
    @code_execution_timer
    def execute_with_parameters(method_to_call, parameters_list):
        return method_to_call(*parameters_list)
