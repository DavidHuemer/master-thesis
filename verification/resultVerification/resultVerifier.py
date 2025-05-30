import threading

from definitions.ast.behavior.behaviorNode import BehaviorNode
from definitions.codeExecution.result.executionResult import ExecutionResult
from definitions.evaluations.csp.parameters.resultParameters import ResultParameters
from definitions.parameters.Variables import Variables
from helper.logs.loggingHelper import log_error
from nodes.baseNodeRunner import BaseNodeRunner
from verification.resultVerification.arrayIndexExecution import ArrayIndexExecution
from verification.resultVerification.infixExecution import InfixExecution
from verification.resultVerification.lengthExecution import LengthExecution
from verification.resultVerification.methodCallExecution import MethodCallExecution
from verification.resultVerification.prefixExecution import PrefixExecution
from verification.resultVerification.quantifier_execution import QuantifierExecution
from verification.resultVerification.questionMarkExecution import QuestionMarkExecution
from verification.resultVerification.resultDto import ResultDto
from verification.resultVerification.terminalExecution import TerminalExecution


class ResultVerifier(BaseNodeRunner[ResultDto]):
    def __init__(self, terminal_execution=None,
                 infix_execution=None, prefix_execution=None,
                 quantifier_execution=None, length_execution=None,
                 method_call_execution=None, array_index_execution=None,
                 question_mark_execution=None):
        super().__init__(
            terminal_handler=terminal_execution or TerminalExecution(),
            infix_handler=infix_execution or InfixExecution(),
            prefix_handler=prefix_execution or PrefixExecution(),
            quantifier_handler=quantifier_execution or QuantifierExecution(),
            length_handler=length_execution or LengthExecution(),
            method_call_handler=method_call_execution or MethodCallExecution(),
            array_index_handler=array_index_execution or ArrayIndexExecution(),
            question_mark_handler=question_mark_execution or QuestionMarkExecution()
        )

    def verify(self, result: ExecutionResult, behavior_node: BehaviorNode, variables: Variables,
               stop_event: threading.Event):

        try:
            # Run through all post conditions and check if they are satisfied
            for post_condition in behavior_node.post_conditions:

                result_dto = ResultDto(node=post_condition,
                                       result=result.result,
                                       variables=variables,
                                       stop_event=stop_event)
                if not self.evaluate(result_dto):
                    return False

            return True
        except Exception as e:
            log_error(f"Error while verifying result: {e}")
            raise e

    def evaluate(self, t: ResultDto):
        return super().evaluate(t)
