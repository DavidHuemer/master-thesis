from nodes.baseNodeRunner import BaseNodeRunner
from nodes.handlers.baseArrayIndexConstraintBuilder import BaseArrayIndexConstraintBuilder
from nodes.handlers.basePrefixConstraintBuilder import BasePrefixConstraintBuilder
from nodes.handlers.baseQuestionMarkConstraintBuilder import BaseQuestionMarkConstraintBuilder
from verification.constraints.arrayLengthConstraintBuilder import ArrayLengthConstraintBuilder
from verification.constraints.constraintsDto import ConstraintsDto
from verification.constraints.infixConstraintBuilder import InfixConstraintBuilder
from verification.constraints.methodCallHandler import MethodCallHandler
from verification.constraints.quantifierConstraintBuilder import QuantifierConstraintBuilder
from verification.constraints.terminalConstraintBuilder import TerminalConstraintBuilder


class ExpressionConstraintBuilder(BaseNodeRunner[ConstraintsDto]):
    def __init__(self, terminal_constraint_builder=TerminalConstraintBuilder(),
                 quantifier_constraint_builder=QuantifierConstraintBuilder(),
                 question_mark_constraint_builder=BaseQuestionMarkConstraintBuilder(),
                 prefix_constraint_builder=BasePrefixConstraintBuilder(),
                 infix_constraint_builder=InfixConstraintBuilder(),
                 array_index_constraint_builder=BaseArrayIndexConstraintBuilder(),
                 array_length_constraint_builder=ArrayLengthConstraintBuilder(),
                 method_call_handler=MethodCallHandler()):
        # noinspection PyTypeChecker
        super().__init__(
            terminal_handler=terminal_constraint_builder,
            quantifier_handler=quantifier_constraint_builder,
            prefix_handler=prefix_constraint_builder,
            question_mark_handler=question_mark_constraint_builder,
            infix_handler=infix_constraint_builder,
            array_index_handler=array_index_constraint_builder,
            length_handler=array_length_constraint_builder,
            method_call_handler=method_call_handler
        )

    def evaluate(self, t: ConstraintsDto):
        base_constraint = super().evaluate(t)
        if base_constraint is not None:
            return base_constraint

        raise Exception("ExpressionConstraintBuilder: Node type not supported")
