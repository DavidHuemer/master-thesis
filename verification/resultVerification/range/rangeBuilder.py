from nodes.baseNodeRunner import BaseNodeRunner
from nodes.handlers.baseArrayIndexConstraintBuilder import BaseArrayIndexConstraintBuilder
from nodes.handlers.basePrefixConstraintBuilder import BasePrefixConstraintBuilder
from nodes.handlers.baseQuestionMarkConstraintBuilder import BaseQuestionMarkConstraintBuilder
from parser.simplifier.quantifier_simplifier.quantifierRangeExecutino import QuantifierRangeExecution
from verification.resultVerification.range.lengthRangeHandler import LengthRangeHandler
from verification.resultVerification.range.rangeDto import RangeDto
from verification.resultVerification.range.rangeInfixHandler import RangeInfixHandler
from verification.resultVerification.terminalExecution import TerminalExecution


class RangeBuilder(BaseNodeRunner[RangeDto]):
    def __init__(self, terminal_execution=TerminalExecution(), infix_range_execution=RangeInfixHandler(),
                 quantifier_range_execution=QuantifierRangeExecution(),
                 question_mark_handler=BaseQuestionMarkConstraintBuilder(),
                 prefix_handler=BasePrefixConstraintBuilder(),
                 array_index_handler=BaseArrayIndexConstraintBuilder(), length_handler=LengthRangeHandler()):
        super().__init__(
            terminal_handler=terminal_execution,
            length_handler=length_handler,
            prefix_handler=prefix_handler,
            quantifier_handler=quantifier_range_execution,
            question_mark_handler=question_mark_handler,
            infix_handler=infix_range_execution,
            array_index_handler=array_index_handler,
            method_call_handler=None
        )

    def evaluate(self, t: RangeDto):
        return super().evaluate(t)
