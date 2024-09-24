from definitions.codeExecution.result.executionResult import ExecutionResult
from definitions.consistencyTestCase import ConsistencyTestCase
from definitions.verification.testCase import TestCase


class CodeExecution:
    @staticmethod
    def execute(test_instance, test_case: TestCase, consistency_test_case: ConsistencyTestCase):
        method_to_call = getattr(test_instance, consistency_test_case.method_info.name)
        parameters = test_case.parameters
        parameters_list = [parameters[param_key] for param_key in parameters]
        return method_to_call(*parameters_list)
