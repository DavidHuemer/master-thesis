from antlr4.tree.Tree import TerminalNodeImpl

import parser.generated.JMLParser as JMLParser
from definitions.ast.expressionNode import ExpressionNode
from definitions.ast.terminalNode import TerminalNode
from definitions.parser.parserResult import ParserResult
from parser.simplifier.arraySimplifier import ArraySimplifier
from parser.simplifier.infixSimplifier import InfixSimplifier
from parser.simplifier.boolQuantifierSimplifier import BoolQuantifierSimplifier
from parser.simplifier.numericQuantifierSimplifier import NumericQuantifierSimplifier
from parser.tree.ruleMetaDataHelper import RuleMetaDataHelper


class RuleSimplifier:
    def __init__(self, rule_meta_data_helper=RuleMetaDataHelper(),
                 bool_quantifier_simplifier=BoolQuantifierSimplifier(),
                 numeric_quantifier_simplifier=NumericQuantifierSimplifier(),
                 array_simplifier=ArraySimplifier(),
                 infix_simplifier=InfixSimplifier()):
        self.rule_meta_data_helper = rule_meta_data_helper
        self.bool_quantifier_simplifier = bool_quantifier_simplifier
        self.numeric_quantifier_simplifier = numeric_quantifier_simplifier
        self.array_simplifier = array_simplifier
        self.infix_simplifier = infix_simplifier

    def simplify_rule(self, rule, parser_result: ParserResult):
        """
        Simplifies a rule
        :param parser_result:
        :param rule: The rule that should be simplified
        :return: The simplified rule
        """

        # TODO: Simplify (shorten) this method

        if isinstance(rule, TerminalNodeImpl):
            return TerminalNode(parser_result.jml_parser.symbolicNames[rule.getSymbol().type], rule.getText())

        meta_data = self.rule_meta_data_helper.get_meta_data_for_rule(rule, parser_result.jml_parser)

        simplified = self.can_simplify(rule, meta_data)
        if simplified is not None:
            return self.simplify_rule(simplified, parser_result)

        if self.is_bool_quantifier(rule):
            return self.bool_quantifier_simplifier.simplify(rule, parser_result, self)

        if self.is_numeric_quantifier(rule):
            return self.numeric_quantifier_simplifier.simplify(rule, parser_result, self)

        # Check if rule is in infix notation a + b. It must have 3 children (left, operator, right)

        arr_val = self.array_simplifier.simplify_array(rule, parser_result, self)
        if arr_val is not None:
            return arr_val

        # check if rule is a terminal node
        if rule.getChildCount() == 0:
            return TerminalNode("Test", rule.getText())

        infix_value = self.infix_simplifier.simplify_infix(rule, parser_result, self)
        if infix_value is not None:
            return infix_value

        node = ExpressionNode(meta_data.name)
        for child in rule.children:
            if isinstance(child, TerminalNodeImpl):
                if meta_data.include_terminal_children():
                    node.add_child(
                        TerminalNode(parser_result.jml_parser.symbolicNames[child.getSymbol().type], child.getText()))
            else:
                node.add_child(self.simplify_rule(child, parser_result))

        return node

    @staticmethod
    def can_simplify(rule, meta_data):
        if rule.getChildCount() == 1 and meta_data.can_simplify():
            return rule.children[0]

        if isinstance(rule, JMLParser.JMLParser.Primary_expressionContext) and rule.getChildCount() == 3:
            return rule.children[1]

        return None

    @staticmethod
    def is_bool_quantifier(rule):
        return isinstance(rule, JMLParser.JMLParser.Bool_quantifier_expressionContext)

    @staticmethod
    def is_numeric_quantifier(rule):
        return isinstance(rule, JMLParser.JMLParser.Numeric_quantifier_expressionContext)
