from definitions.ast.behavior.behaviorNode import BehaviorNode
from definitions.ast.behavior.behaviorType import BehaviorType
from definitions.codeExecution.result.executionResult import ExecutionResult
from definitions.consistencyTestCase import ConsistencyTestCase
from definitions.verification.testCase import TestCase
from helper.logs.loggingHelper import LoggingHelper
from verification.resultVerification.resultVerifier import ResultVerifier


class ExecutionVerifier:
    """
    This class is responsible for verifying the execution of a test case
    """

    def __init__(self, result_verifier=ResultVerifier()):
        self.result_verifier = result_verifier

    def verify(self, execution_result: ExecutionResult, consistency_test_case: ConsistencyTestCase,
    behavior: BehaviorNode, expected_exception, test_case: TestCase):
        try:
            if execution_result.exception is not None:
                result = execution_result.exception
                verification_result = self.verify_exception(exception=execution_result.exception,
                                                            behavior_type=behavior.behavior_type,
                                                            expected_exception=expected_exception)
            else:
                result = execution_result.result
                verification_result = self.verify_result(execution_result=execution_result, behavior=behavior)

            self.log_result(consistency_test_case, test_case, result, verification_result)
            return verification_result
        except Exception as e:
            self.log_result(consistency_test_case, test_case, execution_result.result, False)
            raise e

    @staticmethod
    def verify_exception(exception, behavior_type: BehaviorType, expected_exception):
        if behavior_type == BehaviorType.NORMAL_BEHAVIOR:
            return False

        if (expected_exception is not None) and expected_exception in exception:
            return True

        # TODO: Check if other exception matches
        return False

    def verify_result(self, execution_result: ExecutionResult, behavior: BehaviorNode):
        if behavior.behavior_type == BehaviorType.EXCEPTIONAL_BEHAVIOR:
            return False

        return self.result_verifier.verify(execution_result, behavior)

    @staticmethod
    def log_result(consistency_test_case: ConsistencyTestCase, test_case: TestCase,
                   result, consistency_result: bool):
        LoggingHelper.log_debug(f'Verified {consistency_test_case.method_info.name} with {test_case.parameters}. '
                                f'Result: {result}.'
                                f'Consistency result: {consistency_result}')
