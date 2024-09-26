from definitions.ast.RangeTreeNode import RangeTreeNode
from definitions.ast.quantifier.boolQuantifierTreeNode import BoolQuantifierTreeNode
from definitions.ast.quantifier.boolQuantifierType import BoolQuantifierType
from definitions.parser.parserResult import ParserResult
from parser.generated import JMLParser
from parser.simplifier.quantifierSimplifier import QuantifierSimplifier


class BoolQuantifierSimplifier:
    def __init__(self, quantifier_simplifier=QuantifierSimplifier()):
        self.quantifier_simplifier = quantifier_simplifier

    def simplify(self, rule, parser_result: ParserResult, jml_simplifier) -> BoolQuantifierTreeNode:
        # If the children count of the rule is greater than 1 raise an error
        if len(rule.children) > 1:
            raise Exception("BoolQuantifierSimplifier: Rule has more than 1 child")

        quantified_expression = rule.children[0]

        if isinstance(quantified_expression, JMLParser.JMLParser.Forall_expressionContext):
            return self.simplify_for_all(quantified_expression, parser_result, jml_simplifier)
        elif isinstance(quantified_expression, JMLParser.JMLParser.Exists_expressionContext):
            return self.simplify_exists(quantified_expression, parser_result, jml_simplifier)
        else:
            raise Exception("BoolQuantifierSimplifier: Rule is not a quantified expression")

    def simplify_for_all(self, rule: JMLParser.JMLParser.Forall_expressionContext, parser_result: ParserResult,
                         jml_simplifier):
        if not isinstance(rule.children[1], JMLParser.JMLParser.Bool_quantifier_core_expressionContext):
            raise Exception("BoolQuantifierSimplifier: ForAll expression does not have a bool quantifier core node")

        return self.generate_bool_quantifier_node('FORALL', BoolQuantifierType.FORALL, rule.children[1], parser_result,
                                                  jml_simplifier)

    def simplify_exists(self, rule: JMLParser.JMLParser.Exists_expressionContext, parser_result: ParserResult,
                        jml_simplifier):
        if not isinstance(rule.children[1], JMLParser.JMLParser.Bool_quantifier_core_expressionContext):
            raise Exception("BoolQuantifierSimplifier: Exists expression does not have a bool quantifier core node")

        return self.generate_bool_quantifier_node('EXISTS', BoolQuantifierType.EXISTS, rule.children[1], parser_result,
                                                  jml_simplifier)

    def generate_bool_quantifier_node(self, name, quantifier_type: BoolQuantifierType,
                                      rule: JMLParser.JMLParser.Bool_quantifier_core_expressionContext,
                                      parser_result: ParserResult, jml_simplifier) -> BoolQuantifierTreeNode:
        # First, get type declarations
        variable_names = self.get_type_declarations(rule)

        # Get Range expressions
        ranges = self.get_range(rule, parser_result, jml_simplifier)

        # Get expressions
        expression = self.get_expression(rule, parser_result, jml_simplifier)

        return BoolQuantifierTreeNode(name, quantifier_type, variable_names, ranges, expression)

    def get_type_declarations(self, rule: JMLParser.JMLParser.Bool_quantifier_core_expressionContext):
        if not isinstance(rule.children[0], JMLParser.JMLParser.Type_declarationsContext):
            raise Exception("BoolQuantifierSimplifier: Bool quantifier core expression does not have type declarations")

        type_declarations = rule.children[0]
        return self.quantifier_simplifier.get_type_declarations(type_declarations)

    def get_range(self, rule: JMLParser.JMLParser.Bool_quantifier_core_expressionContext, parser_result: ParserResult,
                  jml_simplifier):
        if not isinstance(rule.range_, JMLParser.JMLParser.Full_range_expressionContext):
            raise Exception("BoolQuantifierSimplifier: Bool quantifier core expression does not have range expression")

        return self.quantifier_simplifier.get_full_range(rule.range_, parser_result, jml_simplifier)

    @staticmethod
    def get_expression(rule: JMLParser.JMLParser.Bool_quantifier_core_expressionContext,
                       parser_result: ParserResult,
                       jml_simplifier):
        if not isinstance(rule.children[4], JMLParser.JMLParser.ExpressionContext):
            raise Exception("BoolQuantifierSimplifier: Bool quantifier core expression does not have an expression")

        return jml_simplifier.simplify_rule(rule.children[4], parser_result)
