import threading

from definitions.ast.behavior.behaviorNode import BehaviorNode
from definitions.codeExecution.result.executionResult import ExecutionResult
from definitions.evaluations.csp.parameters.resultParameters import ResultParameters
from helper.infixHelper import InfixHelper
from helper.logs.loggingHelper import LoggingHelper
from nodes.baseNodeRunner import BaseNodeRunner
from verification.resultVerification.arrayIndexExecution import ArrayIndexExecution
from verification.resultVerification.boolQuantifierExecution import BoolQuantifierExecution
from verification.resultVerification.infixExecution import InfixExecution
from verification.resultVerification.lengthExecution import LengthExecution
from verification.resultVerification.methodCallExecution import MethodCallExecution
from verification.resultVerification.numQuantifierExecution import NumQuantifierExecution
from verification.resultVerification.prefixExecution import PrefixExecution
from verification.resultVerification.quantifier_execution import QuantifierExecution
from verification.resultVerification.questionMarkExecution import QuestionMarkExecution
from verification.resultVerification.resultDto import ResultDto
from verification.resultVerification.terminalExecution import TerminalExecution


class ResultVerifier(BaseNodeRunner[ResultDto]):
    def __init__(self, terminal_execution=TerminalExecution(), bool_quantifier_execution=BoolQuantifierExecution(),
                 num_quantifier_execution=NumQuantifierExecution(), infix_helper=InfixHelper(),
                 infix_execution=InfixExecution(), prefix_execution=PrefixExecution(),
                 quantifier_execution=QuantifierExecution(), length_execution=LengthExecution(),
                 method_call_execution=MethodCallExecution(), array_index_execution=ArrayIndexExecution(),
                 question_mark_execution=QuestionMarkExecution()):
        super().__init__(
            terminal_handler=terminal_execution,
            infix_handler=infix_execution,
            prefix_handler=prefix_execution,
            quantifier_handler=quantifier_execution,
            length_handler=length_execution,
            method_call_handler=method_call_execution,
            array_index_handler=array_index_execution,
            question_mark_handler=question_mark_execution
        )
        self.bool_quantifier_execution = bool_quantifier_execution
        self.num_quantifier_execution = num_quantifier_execution
        self.infix_helper = infix_helper

    def verify(self, result: ExecutionResult, behavior_node: BehaviorNode, result_parameters: ResultParameters,
               stop_event: threading.Event):
        try:
            # Run through all post conditions and check if they are satisfied
            for post_condition in behavior_node.post_conditions:

                result_dto = ResultDto(node=post_condition,
                                       result=result.result,
                                       result_parameters=result_parameters,
                                       result_verifier=self,
                                       stop_event=stop_event)
                if not self.evaluate(result_dto):
                    return False

            return True
        except Exception as e:
            LoggingHelper.log_error(f"Error while verifying result: {e}")
            raise e

    def evaluate(self, t: ResultDto):
        return super().evaluate(t)
