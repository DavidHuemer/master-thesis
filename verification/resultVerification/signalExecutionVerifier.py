import threading

from definitions.ast.behavior.behaviorNode import BehaviorNode
from definitions.ast.behavior.behaviorType import BehaviorType
from definitions.ast.exceptionExpression import ExceptionExpression
from definitions.codeExecution.result.executionException import ExecutionException
from definitions.evaluations.csp.parameters.resultParameters import ResultParameters
from verification.resultVerification.exceptionVerificationUtil import verify_exception_subclass, \
    is_exception_type_allowed
from verification.resultVerification.resultDto import ResultDto
from verification.resultVerification.resultVerifier import ResultVerifier


class SignalExecutionVerifier:
    def __init__(self, result_verifier=ResultVerifier()):
        self.result_verifier = result_verifier

    def verify_signal(self, exception: ExecutionException,
                      behavior: BehaviorNode,
                      expected_exception: str | None,
                      signals: list[ExceptionExpression],
                      result_parameters: ResultParameters, stop_event: threading.Event):
        if behavior.behavior_type == BehaviorType.NORMAL_BEHAVIOR:
            return False

        if not is_exception_type_allowed(exception, behavior.allowed_signals):
            return False

        if expected_exception is not None:
            result = verify_exception_subclass(exception, expected_exception)
            if not result:
                return self.verify_signals(exception, signals, result_parameters, stop_event=stop_event)
            return result

        # Check if other signals matches
        return self.verify_signals(exception, signals, result_parameters, stop_event=stop_event)

    def verify_signals(self, exception: ExecutionException, signals: list[ExceptionExpression],
                       result_parameters: ResultParameters, stop_event: threading.Event):
        for signal_condition in signals:
            t = ResultDto(node=signal_condition.expression, result_parameters=result_parameters, result=None,
                          stop_event=stop_event)

            if (verify_exception_subclass(exception, signal_condition.exception_type) and
                    self.result_verifier.evaluate(t)):
                return True

        return True
