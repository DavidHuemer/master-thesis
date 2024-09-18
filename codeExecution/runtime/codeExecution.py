from definitions.codeExecution.result.executionResult import ExecutionResult
from definitions.inconsistencyTestCase import InconsistencyTestCase
from definitions.verification.testCase import TestCase


class CodeExecution:
    @staticmethod
    def execute(test_instance, test_case: TestCase, inconsistency_test_case: InconsistencyTestCase):
        method_to_call = getattr(test_instance, inconsistency_test_case.method_info.name)
        parameters = test_case.parameters
        parameters_list = [parameters[param_key] for param_key in parameters]
        return method_to_call(*parameters_list)
