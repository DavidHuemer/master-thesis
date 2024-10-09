from nodes.baseNodeRunner import BaseNodeRunner
from verification.constraints.arrayIndexConstraintBuilder import ArrayIndexConstraintBuilder
from verification.constraints.arrayLengthConstraintBuilder import ArrayLengthConstraintBuilder
from verification.constraints.constraintsDto import ConstraintsDto
from verification.constraints.infixConstraintBuilder import InfixConstraintBuilder
from verification.constraints.methodCallHandler import MethodCallHandler
from verification.constraints.prefixConstraintBuilder import PrefixConstraintBuilder
from verification.constraints.quantifierConstraintBuilder import QuantifierConstraintBuilder
from verification.constraints.questionMarkConstraintBuilder import QuestionMarkConstraintBuilder
from verification.constraints.terminalConstraintBuilder import TerminalConstraintBuilder


class ExpressionConstraintBuilder(BaseNodeRunner[ConstraintsDto]):
    def __init__(self, terminal_constraint_builder=TerminalConstraintBuilder(),
                 quantifier_constraint_builder=QuantifierConstraintBuilder(),
                 question_mark_constraint_builder=QuestionMarkConstraintBuilder(),
                 prefix_constraint_builder=PrefixConstraintBuilder(),
                 infix_constraint_builder=InfixConstraintBuilder(),
                 array_index_constraint_builder=ArrayIndexConstraintBuilder(),
                 array_length_constraint_builder=ArrayLengthConstraintBuilder(),
                 method_call_handler=MethodCallHandler()):
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
