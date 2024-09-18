from definitions.ast.RangeTreeNode import RangeTreeNode
from definitions.ast.boolQuantifierTreeNode import BoolQuantifierTreeNode
from definitions.parser.parserResult import ParserResult
from parser.generated import JMLParser


class BoolQuantifierSimplifier:
    def __init__(self):
        pass

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

        return self.generate_bool_quantifier_node('FORALL', rule.children[1], parser_result, jml_simplifier)

    def simplify_exists(self, rule: JMLParser.JMLParser.Exists_expressionContext, parser_result: ParserResult,
                        jml_simplifier):
        if not isinstance(rule.children[1], JMLParser.JMLParser.Bool_quantifier_core_expressionContext):
            raise Exception("BoolQuantifierSimplifier: Exists expression does not have a bool quantifier core node")

        return self.generate_bool_quantifier_node('EXISTS', rule.children[1], parser_result, jml_simplifier)

    def generate_bool_quantifier_node(self, name, rule: JMLParser.JMLParser.Bool_quantifier_core_expressionContext,
                                      parser_result: ParserResult, jml_simplifier) -> BoolQuantifierTreeNode:
        # First, get type declarations
        variable_names = self.get_type_declarations(rule)

        # Get Range expressions
        ranges = self.get_ranges(rule, parser_result, jml_simplifier)

        # Get expressions
        expression = self.get_expression(rule, parser_result, jml_simplifier)

        return BoolQuantifierTreeNode(name, variable_names, ranges, expression)

    @staticmethod
    def get_type_declarations(rule: JMLParser.JMLParser.Bool_quantifier_core_expressionContext):
        if not isinstance(rule.children[0], JMLParser.JMLParser.Type_declarationsContext):
            raise Exception("BoolQuantifierSimplifier: Bool quantifier core expression does not have type declarations")

        type_declarations = rule.children[0]
        variable_names = []

        for type_declaration in type_declarations.children:
            # Type is the first child of the type declaration
            t = type_declaration.children[0].getText()

            # All other children are variable names
            for i in range(1, len(type_declaration.children)):
                variable_names.append((t, type_declaration.children[i].getText()))

        return variable_names

    @staticmethod
    def get_ranges(rule: JMLParser.JMLParser.Bool_quantifier_core_expressionContext, parser_result: ParserResult,
                   jml_simplifier):
        if not isinstance(rule.children[2], JMLParser.JMLParser.Range_expressionContext):
            raise Exception("BoolQuantifierSimplifier: Bool quantifier core expression does not have range expression")

        range_expression = rule.children[2]

        # Run through all children of range_expression that are single_range_expression
        single_ranges = list(filter(lambda x: isinstance(x, JMLParser.JMLParser.Single_range_expressionContext),
                                    range_expression.children))

        ranges: list[RangeTreeNode] = []

        for single_range in single_ranges:
            if hasattr(single_range, "left") and hasattr(single_range, "right"):
                # Check that left is start range comparison
                if not isinstance(single_range.left, JMLParser.JMLParser.Start_range_comparisonContext):
                    raise Exception("BoolQuantifierSimplifier: Range expression does not have start range comparison")

                # Check that right is end range comparison
                if not isinstance(single_range.right, JMLParser.JMLParser.End_range_comparisonContext):
                    raise Exception("BoolQuantifierSimplifier: Range expression does not have end range comparison")

                left = single_range.left
                right = single_range.right

                if not hasattr(left, "ident"):
                    raise Exception("BoolQuantifierSimplifier: Range expression does not have an identifier")

                if not hasattr(left, "op"):
                    raise Exception("BoolQuantifierSimplifier: Range expression does not have an operator")

                if not hasattr(left, "expr"):
                    raise Exception("BoolQuantifierSimplifier: Range expression does not have an expression")

                if not hasattr(right, "ident"):
                    raise Exception("BoolQuantifierSimplifier: Range expression does not have an identifier")

                if not hasattr(right, "op"):
                    raise Exception("BoolQuantifierSimplifier: Range expression does not have an operator")

                if not hasattr(right, "expr"):
                    raise Exception("BoolQuantifierSimplifier: Range expression does not have an expression")

                left_ident = left.ident.text
                right_ident = right.ident.text

                if left_ident != right_ident:
                    raise Exception("BoolQuantifierSimplifier: Range expression does not have the same identifier")

                left_op = left.op.text
                right_op = right.op.text

                left_expr = jml_simplifier.simplify_rule(left.expr, parser_result)
                right_expr = jml_simplifier.simplify_rule(right.expr, parser_result)
                range_node = RangeTreeNode(left_ident, left_expr, right_expr, left_op, right_op)
                ranges.append(range_node)

        return ranges

    @staticmethod
    def get_expression(rule: JMLParser.JMLParser.Bool_quantifier_core_expressionContext,
                       parser_result: ParserResult,
                       jml_simplifier):
        if not isinstance(rule.children[4], JMLParser.JMLParser.ExpressionContext):
            raise Exception("BoolQuantifierSimplifier: Bool quantifier core expression does not have an expression")

        return jml_simplifier.simplify_rule(rule.children[4], parser_result)
