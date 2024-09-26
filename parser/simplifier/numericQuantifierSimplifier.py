from definitions.ast.quantifier.fullRangeTreeNode import FullRangeTreeNode
from definitions.ast.quantifier.numQuantifierTreeNode import NumQuantifierTreeNode
from definitions.parser.parserResult import ParserResult
from parser.generated import JMLParser
from definitions.ast.quantifier.numericQuantifierType import NumericQuantifierType
from definitions.ast.quantifier.numericQuantifierExpressionType import NumericQuantifierExpressionType
from parser.simplifier.quantifierSimplifier import QuantifierSimplifier


class NumericQuantifierSimplifier:
    def __init__(self, quantifier_simplifier=QuantifierSimplifier()):
        self.quantifier_simplifier = quantifier_simplifier

    def simplify(self, rule, parser_result: ParserResult, jml_simplifier):
        if len(rule.children) > 1:
            raise Exception("NumericQuantifierSimplifier: Rule has more than 1 child")

        quantified_expression = rule.children[0]

        if isinstance(quantified_expression, JMLParser.JMLParser.Max_quantifier_expressionContext):
            return self.simplify_generic(NumericQuantifierType.MAX, quantified_expression, parser_result,
                                         jml_simplifier)
        elif isinstance(quantified_expression, JMLParser.JMLParser.Min_quantifier_expressionContext):
            return self.simplify_generic(NumericQuantifierType.MIN, quantified_expression, parser_result,
                                         jml_simplifier)
        elif isinstance(quantified_expression, JMLParser.JMLParser.Sum_quantifier_expressionContext):
            return self.simplify_generic(NumericQuantifierType.SUM, quantified_expression, parser_result,
                                         jml_simplifier)
        elif isinstance(quantified_expression, JMLParser.JMLParser.Product_quantifier_expressionContext):
            return self.simplify_generic(NumericQuantifierType.PRODUCT, quantified_expression, parser_result,
                                         jml_simplifier)
        else:
            raise Exception("NumericQuantifierSimplifier: Rule is not a quantified expression")

    def simplify_generic(self, quantifier_type: NumericQuantifierType, rule, parser_result: ParserResult,
                         jml_simplifier):
        if not isinstance(rule.children[1], JMLParser.JMLParser.Numeric_quantifier_core_expressionContext):
            raise Exception("NumericQuantifierSimplifier: Rule does not have a numeric quantifier core node")

        return self.generate(quantifier_type.value, quantifier_type, rule.children[1], parser_result, jml_simplifier)

    def generate(self, name: str, quantifier_type: NumericQuantifierType,
                 expr: JMLParser.JMLParser.Numeric_quantifier_core_expressionContext, parser_result,
                 jml_simplifier):
        # Check if it is a IDENTIFIER or range expression
        if isinstance(expr.children[0], JMLParser.JMLParser.Numeric_quantifier_value_expressionContext):
            # It is an identifier
            return self.generate_with_value(name, quantifier_type, expr.children[0], parser_result, jml_simplifier)
        elif isinstance(expr.children[0], JMLParser.JMLParser.Numeric_quantifier_range_core_expressionContext):
            # It is a range expression
            return self.generate_with_range(name, quantifier_type, expr.children[0], parser_result, jml_simplifier)
        else:
            raise Exception("NumericQuantifierSimplifier: Rule is not a quantified expression")

    @staticmethod
    def generate_with_value(name: str, quantifier_type: NumericQuantifierType,
                            expr: JMLParser.JMLParser.Numeric_quantifier_value_expressionContext,
                            parser_result, jml_simplifier) \
            -> NumQuantifierTreeNode:
        if hasattr(expr, 'value'):
            value = jml_simplifier.simplify_rule(expr.value, parser_result)

            return NumQuantifierTreeNode(name, quantifier_type, NumericQuantifierExpressionType.VALUE, value)

    def generate_with_range(self, name: str, quantifier_type: NumericQuantifierType,
                            expr: JMLParser.JMLParser.Numeric_quantifier_range_core_expressionContext,
                            parser_result, jml_simplifier):
        variable_names = self.get_type_declarations(expr)
        range_ = self.get_range(expr, parser_result, jml_simplifier)
        expression = self.get_expression(expr, parser_result, jml_simplifier)

        return NumQuantifierTreeNode(name, quantifier_type, NumericQuantifierExpressionType.RANGE, expression,
                                     variable_names, range_)

    def get_type_declarations(self, rule: JMLParser.JMLParser.Numeric_quantifier_range_core_expressionContext):
        if not isinstance(rule.types, JMLParser.JMLParser.Type_declarationsContext):
            raise Exception(
                "NumericQuantifierSimplifier: Numeric quantifier core expression does not have type declarations")
        return self.quantifier_simplifier.get_type_declarations(rule.types)

    def get_range(self, rule: JMLParser.JMLParser.Numeric_quantifier_range_core_expressionContext,
                  parser_result: ParserResult, jml_simplifier) -> FullRangeTreeNode:
        if not isinstance(rule.range_, JMLParser.JMLParser.Full_range_expressionContext):
            raise Exception(
                "NumericQuantifierSimplifier: Numeric quantifier core expression does not have range expression")

        return self.quantifier_simplifier.get_full_range(rule.range_, parser_result, jml_simplifier)

    @staticmethod
    def get_expression(rule: JMLParser.JMLParser.Numeric_quantifier_range_core_expressionContext,
                       parser_result: ParserResult, jml_simplifier):
        if not isinstance(rule.children[4], JMLParser.JMLParser.ExpressionContext):
            raise Exception("BoolQuantifierSimplifier: Bool quantifier core expression does not have an expression")

        return jml_simplifier.simplify_rule(rule.children[4], parser_result)
