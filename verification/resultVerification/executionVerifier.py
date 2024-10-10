from definitions.ast.behavior.behaviorNode import BehaviorNode
from definitions.ast.behavior.behaviorType import BehaviorType
from definitions.ast.exceptionExpression import ExceptionExpression
from definitions.codeExecution.result.executionResult import ExecutionResult
from definitions.codeExecution.result.resultInstances import ResultInstances
from definitions.consistencyTestCase import ConsistencyTestCase
from definitions.evaluations.csp.parameters.resultParameters import ResultParameters
from definitions.verification.testCase import TestCase
from helper.logs.loggingHelper import LoggingHelper
from verification.resultVerification.resultDto import ResultDto
from verification.resultVerification.resultVerifier import ResultVerifier


class ExecutionVerifier:
    """
    This class is responsible for verifying the execution of a test case
    """

    def __init__(self, result_verifier=ResultVerifier()):
        self.result_verifier = result_verifier

    def verify(self, execution_result: ExecutionResult,
               result_parameters: ResultParameters,
               consistency_test_case: ConsistencyTestCase,
               behavior: BehaviorNode, expected_exception, test_case: TestCase,
               result_instances: ResultInstances):
        try:
            if execution_result.exception is not None:
                result = execution_result.exception
                verification_result = self.verify_exception(exception=execution_result.exception,
                                                            execution_result=execution_result,
                                                            behavior_type=behavior.behavior_type,
                                                            expected_exception=expected_exception,
                                                            signal_conditions=behavior.signals_conditions)
            else:
                result = execution_result.result
                verification_result = self.verify_result(execution_result=execution_result,
                                                         behavior=behavior,
                                                         result_parameters=result_parameters)

            self.log_result(consistency_test_case, test_case, result, verification_result)
            return verification_result
        except Exception as e:
            self.log_result(consistency_test_case, test_case, execution_result.result, False)
            raise e

    def verify_exception(self, exception, execution_result: ExecutionResult,
                         behavior_type: BehaviorType, expected_exception,
                         signal_conditions: list[ExceptionExpression]):
        if behavior_type == BehaviorType.NORMAL_BEHAVIOR:
            return False

        if (expected_exception is not None) and expected_exception in exception:
            return True

        # TODO: Check if other exception matches
        for signal_condition in signal_conditions:
            if (signal_condition.name in exception
                    and self.result_verifier.evaluate(execution_result, signal_condition.expression)):
                return True

        return False

    def verify_result(self, execution_result: ExecutionResult, behavior: BehaviorNode,
                      result_parameters: ResultParameters):
        if behavior.behavior_type == BehaviorType.EXCEPTIONAL_BEHAVIOR:
            return False

        return self.result_verifier.verify(execution_result, behavior, result_parameters)

    @staticmethod
    def log_result(consistency_test_case: ConsistencyTestCase, test_case: TestCase,
                   result, consistency_result: bool):
        LoggingHelper.log_debug(f'Verified {consistency_test_case.method_info.name} with {test_case.parameters}. '
                                f'Result: {result}.'
                                f'Consistency result: {consistency_result}')
