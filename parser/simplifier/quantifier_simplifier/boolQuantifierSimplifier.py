from __future__ import annotations

from parser.generated import JMLParser

from definitions.ast.quantifier.boolQuantifierTreeNode import BoolQuantifierTreeNode
from definitions.ast.quantifier.boolQuantifierType import BoolQuantifierType
from nodes.baseNodeHandler import BaseNodeHandler
from parser.simplificationDto import SimplificationDto
from parser.simplifier.quantifier_simplifier.quantifierRangeSimplifier import QuantifierRangeSimplifier


class BoolQuantifierSimplifier(BaseNodeHandler[SimplificationDto]):
    def __init__(self, quantifier_simplifier=QuantifierRangeSimplifier()):
        super().__init__()
        self.quantifier_simplifier = quantifier_simplifier

    def is_node(self, t: SimplificationDto):
        return isinstance(t.node.children[0], JMLParser.JMLParser.Bool_quantifier_expressionContext)

    def handle(self, t: SimplificationDto):
        quantified_expression = t.node.children[0].children[0]

        if isinstance(quantified_expression, JMLParser.JMLParser.Forall_expressionContext):
            return self.simplify_for_all(quantified_expression, t)
        elif isinstance(quantified_expression, JMLParser.JMLParser.Exists_expressionContext):
            return self.simplify_exists(quantified_expression, t)
        else:
            raise Exception("BoolQuantifierSimplifier: Rule is not a quantified expression")

    def simplify_for_all(self, forall_expr: JMLParser.JMLParser.Forall_expressionContext, t: SimplificationDto):
        if not isinstance(forall_expr.expr, JMLParser.JMLParser.Bool_quantifier_core_expressionContext):
            raise Exception("BoolQuantifierSimplifier: ForAll expression does not have a bool quantifier core node")

        return self.generate_bool_quantifier_node('FORALL', BoolQuantifierType.FORALL, forall_expr, t)

    def simplify_exists(self, exists_expr: JMLParser.JMLParser.Exists_expressionContext, t: SimplificationDto):
        if not isinstance(exists_expr.expr, JMLParser.JMLParser.Bool_quantifier_core_expressionContext):
            raise Exception("BoolQuantifierSimplifier: Exists expression does not have a bool quantifier core node")

        return self.generate_bool_quantifier_node('EXISTS', BoolQuantifierType.EXISTS, exists_expr, t)

    def generate_bool_quantifier_node(self, name, quantifier_type: BoolQuantifierType,
                                      rule, t: SimplificationDto) -> BoolQuantifierTreeNode:
        core_expr = rule.expr

        # First, get type declarations
        variable_names = self.get_type_declarations(core_expr)

        # Get Range expressions
        ranges = self.get_range(core_expr, t)

        # Get expressions
        expression = self.get_expression(core_expr, t)

        return BoolQuantifierTreeNode(name, quantifier_type, variable_names, ranges, expression)

    def get_type_declarations(self, rule: JMLParser.JMLParser.Bool_quantifier_core_expressionContext):
        if not isinstance(rule.children[0], JMLParser.JMLParser.Type_declarationsContext):
            raise Exception("BoolQuantifierSimplifier: Bool quantifier core expression does not have type declarations")

        type_declarations = rule.children[0]
        return self.quantifier_simplifier.get_type_declarations(type_declarations)

    def get_range(self, core_expr: JMLParser.JMLParser.RULE_bool_quantifier_core_expression, t: SimplificationDto):
        return self.evaluate_with_runner(t, core_expr.ranges)

    def get_expression(self, rule: JMLParser.JMLParser.Bool_quantifier_core_expressionContext, t: SimplificationDto):
        if not isinstance(rule.expr, JMLParser.JMLParser.ExpressionContext):
            raise Exception("BoolQuantifierSimplifier: Bool quantifier core expression does not have an expression")
        return self.evaluate_with_runner(t, rule.expr)
