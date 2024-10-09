from __future__ import annotations

import parser.generated.JMLParser as JMLParser

from definitions.ast.astTreeNode import AstTreeNode
from nodes.baseNodeRunner import BaseNodeRunner
from parser.simplifier.arrayIndexSimplifier import ArrayIndexSimplifier
from parser.simplifier.exceptionSimplifier import ExceptionSimplifier
from parser.simplifier.infixSimplifier import InfixSimplifier
from parser.simplifier.lengthSimplifier import LengthSimplifier
from parser.simplifier.methodCallSimplifier import MethodCallSimplifier
from parser.simplifier.prefixSimplifier import PrefixSimplifier
from parser.simplifier.quantifier_simplifier.quantifierSimplifier import QuantifierSimplifier
from parser.simplifier.questionMarkExpressionSimplifier import QuestionMarkExpressionSimplifier
from parser.simplifier.referenceSimplifier import ReferenceSimplifier
from parser.simplifier.simplifierDto import SimplifierDto
from parser.simplifier.terminalSimplifier import TerminalSimplifier


class RuleSimplifier(BaseNodeRunner[SimplifierDto]):
    def __init__(self, terminal_simplifier=TerminalSimplifier(),
                 quantifier_simplifier=QuantifierSimplifier(),
                 array_index_simplifier=ArrayIndexSimplifier(),
                 length_simplifier=LengthSimplifier(),
                 infix_simplifier=InfixSimplifier(),
                 exception_simplifier=ExceptionSimplifier(),
                 question_mark_expression_simplifier=QuestionMarkExpressionSimplifier(),
                 reference_simplifier=ReferenceSimplifier(),
                 method_simplifier=MethodCallSimplifier(),
                 prefix_simplifier=PrefixSimplifier()):
        super().__init__(
            terminal_handler=terminal_simplifier,
            infix_handler=infix_simplifier,
            quantifier_handler=quantifier_simplifier,
            question_mark_handler=question_mark_expression_simplifier,
            prefix_handler=prefix_simplifier,
            array_index_handler=array_index_simplifier,
            length_handler=length_simplifier,
            reference_handler=reference_simplifier,
            method_call_handler=method_simplifier
        )
        self.exception_simplifier = exception_simplifier

    def evaluate(self, t: SimplifierDto):
        base_eval_result = super().evaluate(t)

        if base_eval_result is not None:
            return base_eval_result

        basic_simplification = self.can_simplify(t)
        if basic_simplification is not None:
            return basic_simplification

        if self.exception_simplifier.is_node(t):
            return self.exception_simplifier.handle(t)

        raise Exception("No simplification option found for rule: " + str(t.rule))

    def can_simplify(self, t: SimplifierDto) -> AstTreeNode | None:
        if t.rule.getChildCount() == 1:
            return self.evaluate(SimplifierDto(t.rule.children[0], t.rule_simplifier, t.parser_result))
        elif isinstance(t.rule, JMLParser.JMLParser.PrimaryContext) and t.rule.getChildCount() == 3:
            return self.evaluate(SimplifierDto(t.rule.children[1], t.rule_simplifier, t.parser_result))
        elif isinstance(t.rule, JMLParser.JMLParser.Atomic_valueContext) and t.rule.getChildCount() == 3:
            return self.evaluate(SimplifierDto(t.rule.children[1], t.rule_simplifier, t.parser_result))

        return None

    @staticmethod
    def is_numeric_quantifier(rule):
        return isinstance(rule, JMLParser.JMLParser.Numeric_quantifier_expressionContext)

    @staticmethod
    def is_exception_node(rule):
        return isinstance(rule, JMLParser.JMLParser.Exception_expressionContext)
