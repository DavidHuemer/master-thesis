import parser.generated.JMLParser as JMLParser
from definitions.ast.arrayIndexNode import ArrayIndexNode
from definitions.ast.arrayLengthNode import ArrayLengthNode
from definitions.parser.parserResult import ParserResult


class ArraySimplifier:
    """
    Simplifies array expressions
    """

    def simplify_array(self, rule, parser_result: ParserResult, rule_simplifier):
        """
        Simplifies array expressions
        :param rule: The rule to simplify
        :param parser_result: The parser result
        :param rule_simplifier: The rule simplifier
        :return: The simplified array expression or None (if the rule is not an array expression)
        """

        arr_value = self.simplify_array_index(rule, parser_result, rule_simplifier)
        if arr_value is not None:
            return arr_value

        arr_value = self.simplify_array_length(rule)
        if arr_value is not None:
            return arr_value

        return None

    @staticmethod
    def simplify_array_index(rule, parser_result: ParserResult, rule_simplifier):
        """
        Simplifies array index expressions
        :param rule: The rule to simplify
        :param parser_result: The parser result
        :param rule_simplifier: The rule simplifier
        :return: The simplified array index expression or None (if the rule is not an array index expression)
        """
        if isinstance(rule, JMLParser.JMLParser.Array_index_expressionContext):
            return ArrayIndexNode(rule.children[0].getText(),
                                  rule_simplifier.simplify_rule(rule.children[2], parser_result)
                                  )
        return None

    @staticmethod
    def simplify_array_length(rule):
        """
        Simplifies array length expressions
        :param rule: The rule to simplify
        :return: The simplified array length expression or None (if the rule is not an array length expression)
        """
        if isinstance(rule, JMLParser.JMLParser.Array_length_expressionContext):
            return ArrayLengthNode(rule.children[0].getText())

        return None
