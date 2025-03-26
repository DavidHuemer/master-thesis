from __future__ import annotations

import parser.generated.JMLParser as JMLParser

from definitions.ast.astTreeNode import AstTreeNode
from nodes.baseNodeRunner import BaseNodeRunner
from parser.simplificationDto import SimplificationDto
from parser.simplifier.arrayIndexSimplifier import ArrayIndexSimplifier
from parser.simplifier.exceptionSimplifier import ExceptionSimplifier
from parser.simplifier.infixSimplifier import InfixSimplifier
from parser.simplifier.lengthSimplifier import LengthSimplifier
from parser.simplifier.methodCallSimplifier import MethodCallSimplifier
from parser.simplifier.prefixSimplifier import PrefixSimplifier
from parser.simplifier.quantifier_simplifier.quantifierSimplifier import QuantifierSimplifier
from parser.simplifier.questionMarkExpressionSimplifier import QuestionMarkExpressionSimplifier
from parser.simplifier.referenceSimplifier import ReferenceSimplifier
from parser.simplifier.terminalSimplifier import TerminalSimplifier


class RuleSimplifier(BaseNodeRunner[SimplificationDto]):
    def __init__(self, terminal_simplifier=None,
                 quantifier_simplifier=None,
                 array_index_simplifier=None,
                 length_simplifier=None,
                 infix_simplifier=None,
                 exception_simplifier=None,
                 question_mark_expression_simplifier=None,
                 reference_simplifier=None,
                 method_simplifier=None,
                 prefix_simplifier=None):
        super().__init__(
            terminal_handler=terminal_simplifier or TerminalSimplifier(),
            infix_handler=infix_simplifier or InfixSimplifier(),
            quantifier_handler=quantifier_simplifier or QuantifierSimplifier(),
            question_mark_handler=question_mark_expression_simplifier or QuestionMarkExpressionSimplifier(),
            prefix_handler=prefix_simplifier or PrefixSimplifier(),
            array_index_handler=array_index_simplifier or ArrayIndexSimplifier(),
            length_handler=length_simplifier or LengthSimplifier(),
            method_call_handler=method_simplifier or MethodCallSimplifier()
        )
        self.exception_simplifier = exception_simplifier or ExceptionSimplifier()
        self.exception_simplifier.set_runner(self)
        self.reference_simplifier = reference_simplifier or ReferenceSimplifier()
        self.reference_simplifier.set_runner(self)

    def evaluate(self, t: SimplificationDto):
        base_eval_result = super().evaluate(t)

        if base_eval_result is not None:
            return base_eval_result

        basic_simplification = self.can_simplify(t)
        if basic_simplification is not None:
            return basic_simplification

        if self.exception_simplifier.is_node(t):
            return self.exception_simplifier.handle(t)

        if self.reference_simplifier.is_node(t):
            return self.reference_simplifier.handle(t)

        raise Exception(f"No simplification option found for rule: {str(t.node)}")

    def can_simplify(self, t: SimplificationDto) -> AstTreeNode | None:
        if t.node.getChildCount() == 1:
            return self.evaluate(t.copy_with_other_node(t.node.getChild(0)))
        elif isinstance(t.node, JMLParser.JMLParser.PrimaryContext) and t.node.getChildCount() == 3:
            return self.evaluate(t.copy_with_other_node(t.node.children[1]))
        elif isinstance(t.node, JMLParser.JMLParser.Atomic_valueContext) and t.node.getChildCount() == 3:
            return self.evaluate(t.copy_with_other_node(t.node.children[1]))

        return None

    @staticmethod
    def is_numeric_quantifier(rule):
        return isinstance(rule, JMLParser.JMLParser.Numeric_quantifier_expressionContext)

    @staticmethod
    def is_exception_node(rule):
        return isinstance(rule, JMLParser.JMLParser.Exception_expressionContext)
