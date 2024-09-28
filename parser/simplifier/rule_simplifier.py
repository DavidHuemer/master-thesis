from typing import Callable, Any

from antlr4.Token import CommonToken
from antlr4.tree.Tree import TerminalNodeImpl

import parser.generated.JMLParser as JMLParser
from definitions.ast.astTreeNode import AstTreeNode
from definitions.ast.expressionNode import ExpressionNode
from definitions.ast.prefixNode import PrefixNode
from definitions.ast.terminalNode import TerminalNode
from definitions.parser.parserResult import ParserResult
from definitions.parser.ruleMetaData import RuleMetaData
from helper.logs.loggingHelper import LoggingHelper
from parser.simplifier.arraySimplifier import ArraySimplifier
from parser.simplifier.exceptionSimplifier import ExceptionSimplifier
from parser.simplifier.infixSimplifier import InfixSimplifier
from parser.simplifier.boolQuantifierSimplifier import BoolQuantifierSimplifier
from parser.simplifier.numericQuantifierSimplifier import NumericQuantifierSimplifier
from parser.simplifier.questionMarkExpressionSimplifier import QuestionMarkExpressionSimplifier
from parser.tree.ruleMetaDataHelper import RuleMetaDataHelper


class RuleSimplifier:
    def __init__(self, rule_meta_data_helper=RuleMetaDataHelper(),
                 bool_quantifier_simplifier=BoolQuantifierSimplifier(),
                 numeric_quantifier_simplifier=NumericQuantifierSimplifier(),
                 array_simplifier=ArraySimplifier(),
                 infix_simplifier=InfixSimplifier(),
                 exception_simplifier=ExceptionSimplifier(),
                 question_mark_expression_simplifier=QuestionMarkExpressionSimplifier()):
        self.rule_meta_data_helper = rule_meta_data_helper
        self.bool_quantifier_simplifier = bool_quantifier_simplifier
        self.numeric_quantifier_simplifier = numeric_quantifier_simplifier
        self.array_simplifier = array_simplifier
        self.infix_simplifier = infix_simplifier
        self.exception_simplifier = exception_simplifier
        self.question_mark_expr_simplifier = question_mark_expression_simplifier

        # list of methods
        self.simplify_options: list[(str, Callable[[Any, RuleMetaData, ParserResult], AstTreeNode | None])] = [
            ("terminal node",
             lambda rule, meta, parser_result: self.can_simplify_terminal_node(rule, parser_result)),
            ("basic simplify",
             lambda rule, meta, parser_result: self.can_simplify(rule, meta, parser_result)),
            ('infix',
             lambda rule, meta, parser_result: self.infix_simplifier.simplify_infix(rule, parser_result, self)),
            ('question_mark',
             lambda rule, meta, parser_result: self.question_mark_expr_simplifier.simplify(rule, parser_result, self)),
            ('exception',
             lambda rule, meta, parser_result: self.exception_simplifier.simplify(rule, parser_result, self)),
            ('quantifier',
             lambda rule, meta, parser_result: self.is_quantifier(rule, parser_result)),
            ('array',
             lambda rule, meta, parser_result: self.array_simplifier.simplify_array(rule, parser_result, self)),
            ('prefix',
             lambda rule, meta, parser_result: self.can_simplify_prefix(rule, meta, parser_result)),
            ('fallback',
             lambda rule, meta, parser_result: self.fallback_simplify(rule, meta, parser_result))
        ]

        print("Hello")

    def simplify_rule(self, rule, parser_result: ParserResult):
        """
        Simplifies a rule
        :param parser_result:
        :param rule: The rule that should be simplified
        :return: The simplified rule
        """

        try:
            meta_data = self.rule_meta_data_helper.get_meta_data_for_rule(rule, parser_result.jml_parser)

            for option in self.simplify_options:
                expr = option[1](rule, meta_data, parser_result)
                if expr is not None:
                    return expr

        except Exception as e:
            print("Error while simplifying rule: " + str(rule))
            raise e

        raise Exception("No simplification option found for rule: " + str(rule))

    @staticmethod
    def can_simplify_terminal_node(rule, parser_result) -> TerminalNode | None:
        if isinstance(rule, TerminalNodeImpl):
            return TerminalNode(parser_result.jml_parser.symbolicNames[rule.getSymbol().type], rule.getText())

        return None

    def can_simplify(self, rule, meta_data, parser_result) -> AstTreeNode | None:
        if rule.getChildCount() == 1 and meta_data.can_simplify():
            return self.simplify_rule(rule.children[0], parser_result)

        if isinstance(rule, JMLParser.JMLParser.PrimaryContext) and rule.getChildCount() == 3:
            return self.simplify_rule(rule.children[1], parser_result)

        if isinstance(rule, JMLParser.JMLParser.Atomic_valueContext) and rule.getChildCount() == 3:
            return self.simplify_rule(rule.children[1], parser_result)

        return None

    def is_quantifier(self, rule, parser_result):
        if self.is_bool_quantifier(rule):
            return self.bool_quantifier_simplifier.simplify(rule, parser_result, self)

        if self.is_numeric_quantifier(rule):
            return self.numeric_quantifier_simplifier.simplify(rule, parser_result, self)

        return None

    @staticmethod
    def is_bool_quantifier(rule):
        return isinstance(rule, JMLParser.JMLParser.Bool_quantifier_expressionContext)

    @staticmethod
    def is_numeric_quantifier(rule):
        return isinstance(rule, JMLParser.JMLParser.Numeric_quantifier_expressionContext)

    @staticmethod
    def is_exception_node(rule):
        return isinstance(rule, JMLParser.JMLParser.Exception_expressionContext)

    def can_simplify_infix(self, rule, meta, parser_result):
        pass

    def fallback_simplify(self, rule, meta, parser_result):
        node = ExpressionNode(meta.name)
        # Check if first child is a terminal node and has the text "-"
        if (rule.getChildCount() > 1
                and isinstance(rule.children[0], TerminalNodeImpl) and rule.children[0].getText() == "-"):
            node.name = "negative_number"
            node.add_child(self.simplify_rule(rule.children[1], parser_result))
            return node

        if (rule.getChildCount() > 1
                and isinstance(rule.children[0], TerminalNodeImpl) and rule.children[0].getText() == "!"):
            node.name = "not_expression"
            node.add_child(self.simplify_rule(rule.children[1], parser_result))
            return node

        for child in rule.children:
            if isinstance(child, TerminalNodeImpl):
                node.add_child(
                    TerminalNode(parser_result.jml_parser.symbolicNames[child.getSymbol().type], child.getText()))
            else:
                node.add_child(self.simplify_rule(child, parser_result))
        return node

    def can_simplify_prefix(self, rule, meta, parser_result):
        if hasattr(rule, "prefix") and rule.prefix is not None and isinstance(rule.prefix, CommonToken):
            prefix = rule.prefix.text
            expr = self.simplify_rule(rule.expr, parser_result)
            return PrefixNode(prefix, expr)

        return None
