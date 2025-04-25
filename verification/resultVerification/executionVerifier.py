import threading

from codetiming import Timer
from jpype import JInt, JString

from definitions.ast.behavior.behaviorNode import BehaviorNode
from definitions.ast.behavior.behaviorType import BehaviorType
from definitions.ast.exceptionExpression import ExceptionExpression
from definitions.codeExecution.result.executionException import ExecutionException
from definitions.codeExecution.result.executionResult import ExecutionResult
from definitions.codeExecution.result.resultInstances import ResultInstances
from definitions.consistencyTestCase import ConsistencyTestCase
from definitions.evaluations.csp.parameters.resultParameters import ResultParameters
from definitions.parameters.Variables import Variables
from definitions.verification.testCase import TestCase
from helper.logs.loggingHelper import log_debug
from util.Singleton import Singleton
from verification.resultVerification.resultVerifier import ResultVerifier
from verification.resultVerification.signalExecutionVerifier import SignalExecutionVerifier


class ExecutionVerifier(Singleton):
    """
    This class is responsible for verifying the execution of a test case
    """

    def __init__(self, result_verifier=None, signal_execution_verifier=None):
        self.result_verifier = result_verifier or ResultVerifier()
        self.signal_execution_verifier = signal_execution_verifier or SignalExecutionVerifier()

    def verify(self, execution_result: ExecutionResult,
               consistency_test_case: ConsistencyTestCase,
               behavior: BehaviorNode, expected_exception, variables: Variables,
               stop_event: threading.Event):

        try:
            if execution_result.exception is None:
                # validate result
                result = execution_result.result
                verification_result = self.verify_result(execution_result=execution_result,
                                                         behavior=behavior,
                                                         variables=variables, stop_event=stop_event)
            else:
                # validate exception
                result = execution_result.exception
                verification_result = self.verify_exception(exception=execution_result.exception,
                                                            behavior=behavior,
                                                            expected_exception=expected_exception,
                                                            signal_conditions=behavior.signals_conditions,
                                                            variables=variables,
                                                            stop_event=stop_event)

            self.log_result(consistency_test_case, variables, result, verification_result)
            return verification_result
        except Exception as e:
            self.log_result(consistency_test_case, variables, execution_result.result, False)
            raise e

    def verify_exception(self, exception: ExecutionException, behavior: BehaviorNode, expected_exception,
                         signal_conditions: list[ExceptionExpression], variables: Variables,
                         stop_event: threading.Event):

        return self.signal_execution_verifier.verify_signal(exception=exception,
                                                            behavior=behavior,
                                                            expected_exception=expected_exception,
                                                            signals=signal_conditions,
                                                            variables=variables,
                                                            stop_event=stop_event)

    def verify_result(self, execution_result: ExecutionResult, behavior: BehaviorNode,
                      variables: Variables, stop_event: threading.Event):
        if behavior.behavior_type == BehaviorType.EXCEPTIONAL_BEHAVIOR:
            return False

        return self.result_verifier.verify(execution_result, behavior, variables, stop_event)

    @staticmethod
    def log_result(consistency_test_case: ConsistencyTestCase, variables: Variables,
                   result, consistency_result: bool):
        # TODO: the actual parameters should be logged

        log_debug(
            f'Verified {consistency_test_case.method_info.name} with {variables.get_method_call_visualization()}. '
            f'Result: {result}.'
            f'Consistency result: {consistency_result}')
