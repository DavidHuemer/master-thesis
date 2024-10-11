from parser.generated import JMLParser

from definitions.ast.astTreeNode import AstTreeNode
from definitions.ast.quantifier.numQuantifierTreeNode import NumQuantifierTreeNode
from definitions.ast.quantifier.numericQuantifierExpressionType import NumericQuantifierExpressionType
from definitions.ast.quantifier.numericQuantifierType import NumericQuantifierType
from nodes.baseNodeHandler import BaseNodeHandler
from parser.simplificationDto import SimplificationDto
from parser.simplifier.quantifier_simplifier.quantifierRangeSimplifier import QuantifierRangeSimplifier

type QuantifierType = (JMLParser.JMLParser.Max_quantifier_expressionContext
                       | JMLParser.JMLParser.Min_quantifier_expressionContext
                       | JMLParser.JMLParser.Sum_quantifier_expressionContext
                       | JMLParser.JMLParser.Product_quantifier_expressionContext)


class NumericQuantifierSimplifier(BaseNodeHandler[SimplificationDto]):
    def __init__(self, quantifier_simplifier=QuantifierRangeSimplifier()):
        self.quantifier_simplifier = quantifier_simplifier

    def is_node(self, t: SimplificationDto):
        return isinstance(t.node.children[0], JMLParser.JMLParser.Numeric_quantifier_expressionContext)

    def handle(self, t: SimplificationDto):
        quantified_expression = t.node.children[0].children[0]

        if isinstance(quantified_expression, JMLParser.JMLParser.Max_quantifier_expressionContext):
            return self.simplify_generic(NumericQuantifierType.MAX, quantified_expression, t)
        elif isinstance(quantified_expression, JMLParser.JMLParser.Min_quantifier_expressionContext):
            return self.simplify_generic(NumericQuantifierType.MIN, quantified_expression, t)
        elif isinstance(quantified_expression, JMLParser.JMLParser.Sum_quantifier_expressionContext):
            return self.simplify_generic(NumericQuantifierType.SUM, quantified_expression, t)
        elif isinstance(quantified_expression, JMLParser.JMLParser.Product_quantifier_expressionContext):
            return self.simplify_generic(NumericQuantifierType.PRODUCT, quantified_expression, t)

    def simplify_generic(self, quantifier_type: NumericQuantifierType,
                         rule: QuantifierType, t: SimplificationDto):
        if not isinstance(rule.expr, JMLParser.JMLParser.Numeric_quantifier_core_expressionContext):
            raise Exception("NumericQuantifierSimplifier: Rule does not have a numeric quantifier core node")

        return self.generate(quantifier_type.value, quantifier_type, rule.expr, t)

    def generate(self, name: str, quantifier_type: NumericQuantifierType,
                 expr: JMLParser.JMLParser.Numeric_quantifier_core_expressionContext, t: SimplificationDto):
        # Check if it is a IDENTIFIER or range expression
        if isinstance(expr.children[0], JMLParser.JMLParser.Numeric_quantifier_values_expressionContext):
            # Simplify by values
            return self.generate_with_value(name, quantifier_type, expr.children[0], t)
        elif isinstance(expr.children[0], JMLParser.JMLParser.Numeric_quantifier_range_core_expressionContext):
            # Simplify by range
            return self.generate_with_range(name, quantifier_type, expr.children[0], t)
        else:
            raise Exception("NumericQuantifierSimplifier: Rule is not a quantified expression")

    @staticmethod
    def generate_with_value(name: str, quantifier_type: NumericQuantifierType,
                            expr: JMLParser.JMLParser.Numeric_quantifier_values_expressionContext,
                            t: SimplificationDto) -> NumQuantifierTreeNode:

        # Filter child values that are instances of Numeric_quantifier_valueContext
        filtered_values = list(filter(lambda x: isinstance(x, JMLParser.JMLParser.ExpressionContext),
                                      expr.children))

        # Get the expressions of the values
        expression_values = [t.evaluate_with_other_node(value) for value in filtered_values]
        return NumQuantifierTreeNode(name, quantifier_type, NumericQuantifierExpressionType.VALUE, expression_values)

    def generate_with_range(self, name: str, quantifier_type: NumericQuantifierType,
                            expr: JMLParser.JMLParser.Numeric_quantifier_range_core_expressionContext,
                            t: SimplificationDto):
        variable_names = self.get_type_declarations(expr)
        range_ = self.get_range(expr, t)
        expression = self.get_expression(expr, t)

        return NumQuantifierTreeNode(name, quantifier_type, NumericQuantifierExpressionType.RANGE, expression,
                                     variable_names, range_)

    def get_type_declarations(self, rule: JMLParser.JMLParser.Numeric_quantifier_range_core_expressionContext):
        if not isinstance(rule.types, JMLParser.JMLParser.Type_declarationsContext):
            raise Exception(
                "NumericQuantifierSimplifier: Numeric quantifier core expression does not have type declarations")
        return self.quantifier_simplifier.get_type_declarations(rule.types)

    @staticmethod
    def get_range(rule: JMLParser.JMLParser.Numeric_quantifier_range_core_expressionContext,
                  t: SimplificationDto) -> AstTreeNode:

        return t.evaluate_with_other_node(rule.ranges)

    @staticmethod
    def get_expression(rule: JMLParser.JMLParser.Numeric_quantifier_range_core_expressionContext,
                       t: SimplificationDto):
        if not isinstance(rule.children[4], JMLParser.JMLParser.ExpressionContext):
            raise Exception("BoolQuantifierSimplifier: Bool quantifier core expression does not have an expression")

        return t.evaluate_with_other_node(rule.children[4])
