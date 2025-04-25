import threading

from definitions.ast.behavior.behaviorNode import BehaviorNode
from definitions.ast.behavior.behaviorType import BehaviorType
from definitions.ast.exceptionExpression import ExceptionExpression
from definitions.codeExecution.result.executionException import ExecutionException
from definitions.evaluations.csp.parameters.resultParameters import ResultParameters
from definitions.parameters import Variables
from verification.resultVerification.exceptionVerificationUtil import verify_exception_subclass, \
    is_exception_type_allowed
from verification.resultVerification.resultDto import ResultDto
from verification.resultVerification.resultVerifier import ResultVerifier


class SignalExecutionVerifier:
    def __init__(self, result_verifier=None):
        self.result_verifier = result_verifier or ResultVerifier()

    def verify_signal(self, exception: ExecutionException,
                      behavior: BehaviorNode,
                      expected_exception: str | None,
                      signals: list[ExceptionExpression],
                      variables: Variables, stop_event: threading.Event):
        if behavior.behavior_type == BehaviorType.NORMAL_BEHAVIOR:
            return False

        if not is_exception_type_allowed(exception, behavior.allowed_signals):
            return False

        if expected_exception is not None:
            result = verify_exception_subclass(exception, expected_exception)
            if not result:
                return self.verify_signals(exception, signals, variables, stop_event=stop_event)
            return result

        # Check if other signals matches
        return self.verify_signals(exception, signals, variables, stop_event=stop_event)

    def verify_signals(self, exception: ExecutionException, signals: list[ExceptionExpression],
                       variables: Variables, stop_event: threading.Event):
        matching_signals = [signal_condition for signal_condition in signals
                            if verify_exception_subclass(exception, signal_condition.exception_type)]

        if len(matching_signals) == 0:
            return True

        return all(
            self.result_verifier.evaluate(
                ResultDto(node=signal_condition.expression,
                          variables=variables,
                          result=None,
                          stop_event=stop_event)
            )
            for signal_condition in matching_signals
        )
