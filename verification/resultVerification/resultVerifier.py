import threading

from definitions.ast.behavior.behaviorNode import BehaviorNode
from definitions.codeExecution.result.executionResult import ExecutionResult
from definitions.evaluations.csp.parameters.resultParameters import ResultParameters
from helper.infixHelper import InfixHelper
from helper.logs.loggingHelper import log_error
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
    def __init__(self, terminal_execution=None, bool_quantifier_execution=None,
                 num_quantifier_execution=None, infix_helper=None,
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
        self.bool_quantifier_execution = bool_quantifier_execution or BoolQuantifierExecution()
        self.num_quantifier_execution = num_quantifier_execution or NumQuantifierExecution()
        self.infix_helper = infix_helper or InfixHelper()

        self.bool_quantifier_execution.set_runner(self)
        self.num_quantifier_execution.set_runner(self)

    def verify(self, result: ExecutionResult, behavior_node: BehaviorNode, result_parameters: ResultParameters,
               stop_event: threading.Event):

        try:
            # Run through all post conditions and check if they are satisfied
            for post_condition in behavior_node.post_conditions:

                result_dto = ResultDto(node=post_condition,
                                       result=result.result,
                                       result_parameters=result_parameters,
                                       stop_event=stop_event)
                if not self.evaluate(result_dto):
                    return False

            return True
        except Exception as e:
            log_error(f"Error while verifying result: {e}")
            raise e

    def evaluate(self, t: ResultDto):
        return super().evaluate(t)
