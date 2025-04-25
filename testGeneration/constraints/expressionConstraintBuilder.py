from nodes.baseNodeRunner import BaseNodeRunner
from nodes.handlers.baseArrayIndexConstraintBuilder import BaseArrayIndexConstraintBuilder
from nodes.handlers.basePrefixConstraintBuilder import BasePrefixConstraintBuilder
from nodes.handlers.baseQuestionMarkConstraintBuilder import BaseQuestionMarkConstraintBuilder
from testGeneration.constraints.arrayLengthConstraintBuilder import ArrayLengthConstraintBuilder
from testGeneration.constraints.constraintsDto import ConstraintsDto
from testGeneration.constraints.infixConstraintBuilder import InfixConstraintBuilder
from testGeneration.constraints.methodCallHandler import MethodCallHandler
from testGeneration.constraints.quantifierConstraintBuilder import QuantifierConstraintBuilder
from testGeneration.constraints.terminalConstraintBuilder import TerminalConstraintBuilder
from util.Singleton import Singleton


class ExpressionConstraintBuilder(BaseNodeRunner[ConstraintsDto], Singleton):
    def __init__(self, terminal_constraint_builder: TerminalConstraintBuilder | None = None,
                 quantifier_constraint_builder: QuantifierConstraintBuilder | None = None,
                 question_mark_constraint_builder: BaseQuestionMarkConstraintBuilder | None = None,
                 prefix_constraint_builder: BasePrefixConstraintBuilder | None = None,
                 infix_constraint_builder: InfixConstraintBuilder | None = None,
                 array_index_constraint_builder: BaseArrayIndexConstraintBuilder | None = None,
                 array_length_constraint_builder: ArrayLengthConstraintBuilder | None = None,
                 method_call_handler: MethodCallHandler | None = None):
        quantifier_constraint_builder = quantifier_constraint_builder or QuantifierConstraintBuilder()
        question_mark_constraint_builder = question_mark_constraint_builder or BaseQuestionMarkConstraintBuilder()
        prefix_constraint_builder = prefix_constraint_builder or BasePrefixConstraintBuilder()
        infix_constraint_builder = infix_constraint_builder or InfixConstraintBuilder()
        array_index_constraint_builder = array_index_constraint_builder or BaseArrayIndexConstraintBuilder()
        array_length_constraint_builder = array_length_constraint_builder or ArrayLengthConstraintBuilder()
        method_call_handler = method_call_handler or MethodCallHandler()

        # noinspection PyTypeChecker
        super().__init__(
            terminal_handler=terminal_constraint_builder or TerminalConstraintBuilder(),
            quantifier_handler=quantifier_constraint_builder,
            prefix_handler=prefix_constraint_builder,
            question_mark_handler=question_mark_constraint_builder,
            infix_handler=infix_constraint_builder,
            array_index_handler=array_index_constraint_builder,
            length_handler=array_length_constraint_builder,
            method_call_handler=method_call_handler
        )

    def evaluate(self, t: ConstraintsDto):
        return super().evaluate(t)
