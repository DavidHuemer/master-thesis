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

        arr_value = self.simplify_array_length(rule, parser_result, rule_simplifier)
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
        if (rule.getChildCount() == 4 and rule.children[1].getText() == '[' and rule.children[3].getText() == ']'
                and hasattr(rule, "expr") and rule.expr is not None
                and hasattr(rule, "index_expr") and rule.index_expr is not None):
            expr = rule_simplifier.simplify_rule(rule.expr, parser_result)
            index_expr = rule_simplifier.simplify_rule(rule.index_expr, parser_result)
            return ArrayIndexNode(expr, index_expr)

        return None

    @staticmethod
    def simplify_array_length(rule, parser_result: ParserResult, rule_simplifier):
        """
        Simplifies array length expressions
        :param rule: The rule to simplify
        :return: The simplified array length expression or None (if the rule is not an array length expression)
        """

        if rule.getChildCount() == 3 and rule.children[1].getText() == '.' and rule.children[2].getText() == 'length':
            arr_expr = rule_simplifier.simplify_rule(rule.children[0], parser_result)
            return ArrayLengthNode(arr_expr)

        return None
