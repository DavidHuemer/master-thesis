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
    def __init__(self, terminal_execution=None, infix_range_execution=None,
                 quantifier_range_execution=None,
                 question_mark_handler=None,
                 prefix_handler=None,
                 array_index_handler=None, length_handler=None):
        super().__init__(
            terminal_handler=terminal_execution or TerminalExecution(),
            length_handler=length_handler or LengthRangeHandler(),
            prefix_handler=prefix_handler or BasePrefixConstraintBuilder(),
            quantifier_handler=quantifier_range_execution or QuantifierRangeExecution(),
            question_mark_handler=question_mark_handler or BaseQuestionMarkConstraintBuilder(),
            infix_handler=infix_range_execution or RangeInfixHandler(),
            array_index_handler=array_index_handler or BaseArrayIndexConstraintBuilder(),
            method_call_handler=None
        )

    def evaluate(self, t: RangeDto):
        return super().evaluate(t)
