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
from definitions.verification.testCase import TestCase
from helper.logs.loggingHelper import log_debug
from util.Singleton import Singleton
from verification.resultVerification.resultVerifier import ResultVerifier
from verification.resultVerification.signalExecutionVerifier import SignalExecutionVerifier

execution_verifier_timer = Timer(name="execution_verifier", logger=None)


class ExecutionVerifier(Singleton):
    """
    This class is responsible for verifying the execution of a test case
    """

    def __init__(self, result_verifier=ResultVerifier(), signal_execution_verifier=SignalExecutionVerifier()):
        self.result_verifier = result_verifier
        self.signal_execution_verifier = signal_execution_verifier

    @execution_verifier_timer
    def verify(self, execution_result: ExecutionResult,
               result_parameters: ResultParameters,
               consistency_test_case: ConsistencyTestCase,
               behavior: BehaviorNode, expected_exception, test_case: TestCase,
               result_instances: ResultInstances, stop_event: threading.Event):

        a = JString("a")
        b = JString("b")
        c = JString("c")
        try:
            if execution_result.exception is not None:
                # Validate exception
                result = execution_result.exception
                verification_result = self.verify_exception(exception=execution_result.exception,
                                                            behavior=behavior,
                                                            expected_exception=expected_exception,
                                                            signal_conditions=behavior.signals_conditions,
                                                            result_parameters=result_parameters,
                                                            stop_event=stop_event)
            else:
                # Validate result
                result = execution_result.result
                verification_result = self.verify_result(execution_result=execution_result,
                                                         behavior=behavior,
                                                         result_parameters=result_parameters, stop_event=stop_event)

            self.log_result(consistency_test_case, test_case, result, verification_result)
            return verification_result
        except Exception as e:
            self.log_result(consistency_test_case, test_case, execution_result.result, False)
            raise e

    def verify_exception(self, exception: ExecutionException, behavior: BehaviorNode, expected_exception,
                         signal_conditions: list[ExceptionExpression], result_parameters: ResultParameters,
                         stop_event: threading.Event):

        return self.signal_execution_verifier.verify_signal(exception=exception,
                                                            behavior=behavior,
                                                            expected_exception=expected_exception,
                                                            signals=signal_conditions,
                                                            result_parameters=result_parameters,
                                                            stop_event=stop_event)

    def verify_result(self, execution_result: ExecutionResult, behavior: BehaviorNode,
                      result_parameters: ResultParameters, stop_event: threading.Event):
        if behavior.behavior_type == BehaviorType.EXCEPTIONAL_BEHAVIOR:
            return False

        return self.result_verifier.verify(execution_result, behavior, result_parameters, stop_event)

    @staticmethod
    def log_result(consistency_test_case: ConsistencyTestCase, test_case: TestCase,
                   result, consistency_result: bool):
        log_debug(f'Verified {consistency_test_case.method_info.name} with {test_case.parameters}. '
                  f'Result: {result}.'
                  f'Consistency result: {consistency_result}')
