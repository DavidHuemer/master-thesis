import threading

import jpype

from definitions.ast.behavior.behaviorNode import BehaviorNode
from definitions.ast.behavior.behaviorType import BehaviorType
from definitions.ast.exceptionExpression import ExceptionExpression
from definitions.codeExecution.result.executionException import ExecutionException
from definitions.evaluations.csp.parameters.resultParameters import ResultParameters
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
        # TODO: Check subclass

        exception_class = jpype.JClass(exception.full_name)
        allowed_exceptions = [jpype.JClass(f'java.lang.{exception}') for exception in behavior.allowed_signals]
        if len(allowed_exceptions) > 0 and not any([issubclass(exception_class, allowed_exception) for allowed_exception in allowed_exceptions]):
            return False

        if expected_exception is not None:
            result = self.verify_exception_subclass(exception, expected_exception)
            if not result:
                return self.verify_signals(exception, signals, result_parameters, stop_event=stop_event)
            return result

        # Check if other signals matches
        return self.verify_signals(exception, signals, result_parameters, stop_event=stop_event)

    @staticmethod
    def verify_exception_subclass(exception: ExecutionException, expected_exception: str):
        expected_exception_instance = jpype.JClass(f'java.lang.{expected_exception}')
        thrown_exception_instance = jpype.JClass(exception.full_name)

        return issubclass(thrown_exception_instance, expected_exception_instance)

    def verify_signals(self, exception: ExecutionException, signals: list[ExceptionExpression],
                       result_parameters: ResultParameters, stop_event: threading.Event):
        for signal_condition in signals:
            t = ResultDto(node=signal_condition.expression, result_verifier=self.result_verifier,
                          result_parameters=result_parameters, result=None, stop_event=stop_event)

            if (self.verify_exception_subclass(exception, signal_condition.exception_type) and
                    self.result_verifier.evaluate(t)):
                return True

        return False
