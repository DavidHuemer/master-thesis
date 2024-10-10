from parser.generated import JMLParser

from definitions.ast.RangeTreeNode import RangeTreeNode
from definitions.ast.quantifier.fullRangeTreeNode import FullRangeTreeNode
from parser.simplifier.simplifierDto import SimplifierDto


class QuantifierRangeSimplifier:
    @staticmethod
    def get_type_declarations(types: JMLParser.JMLParser.Type_declarationsContext):
        variable_names = []

        for type_declaration in types.children:
            # Type is the first child of the type declaration
            t = type_declaration.children[0].getText()

            # All other children are variable names
            for i in range(1, len(type_declaration.children)):
                if type_declaration.children[i].getText() == ',':
                    continue
                variable_names.append((t, type_declaration.children[i].getText()))

        return variable_names

    def get_full_range(self, range_expression,
                       t: SimplifierDto) -> FullRangeTreeNode:

        # if not isinstance(range_expression.ranges, JMLParser.JMLParser.Range_expressionContext):
        #     raise Exception("BoolQuantifierSimplifier: Range expression does not have range expression")

        ranges = self.get_ranges(range_expression.ranges, t)

        # The expressions are not terminal nodes of the range_expression.children (+1)

        if range_expression.expr is not None:
            expr = self.get_range_predicate(range_expression.expr, t)
        else:
            expr = None

        return FullRangeTreeNode(ranges, expr)

    @staticmethod
    def get_range_predicate(expr, t: SimplifierDto):
        if hasattr(expr, 'expr'):
            return t.rule_simplifier.evaluate(
                SimplifierDto(expr.expr, t.rule_simplifier, parser_result=t.parser_result))
        else:
            return None

    @staticmethod
    def get_ranges(range_expression,
                   t: SimplifierDto) -> list[RangeTreeNode]:
        ranges: list[RangeTreeNode] = []

        # single_ranges = list(filter(lambda x: isinstance(x, JMLParser.JMLParser.Single_range_expressionContext),
        #                             range_expression.children))
        #
        # for single_range in single_ranges:
        #     if hasattr(single_range, "left") and hasattr(single_range, "right"):
        #         # Check that left is start range comparison
        #         if not isinstance(single_range.left, JMLParser.JMLParser.Start_range_comparisonContext):
        #             raise Exception("BoolQuantifierSimplifier: Range expression does not have start range comparison")
        #
        #         # Check that right is end range comparison
        #         if not isinstance(single_range.right, JMLParser.JMLParser.End_range_comparisonContext):
        #             raise Exception("BoolQuantifierSimplifier: Range expression does not have end range comparison")
        #
        #         left = single_range.left
        #         right = single_range.right
        #
        #         if not hasattr(left, "ident"):
        #             raise Exception("BoolQuantifierSimplifier: Range expression does not have an identifier")
        #
        #         if not hasattr(left, "op"):
        #             raise Exception("BoolQuantifierSimplifier: Range expression does not have an operator")
        #
        #         if not hasattr(left, "expr"):
        #             raise Exception("BoolQuantifierSimplifier: Range expression does not have an expression")
        #
        #         if not hasattr(right, "ident"):
        #             raise Exception("BoolQuantifierSimplifier: Range expression does not have an identifier")
        #
        #         if not hasattr(right, "op"):
        #             raise Exception("BoolQuantifierSimplifier: Range expression does not have an operator")
        #
        #         if not hasattr(right, "expr"):
        #             raise Exception("BoolQuantifierSimplifier: Range expression does not have an expression")
        #
        #         left_ident = left.ident.text
        #         right_ident = right.ident.text
        #
        #         if left_ident != right_ident:
        #             raise Exception("BoolQuantifierSimplifier: Range expression does not have the same identifier")
        #
        #         left_op = left.op.text
        #         right_op = right.op.text
        #
        #         left_expr = t.rule_simplifier.evaluate(SimplifierDto(left.expr, t.rule_simplifier, t.parser_result))
        #         right_expr = t.rule_simplifier.evaluate(SimplifierDto(right.expr, t.rule_simplifier, t.parser_result))
        #         range_node = RangeTreeNode(left_ident, left_expr, right_expr, left_op, right_op)
        #         ranges.append(range_node)

        return ranges
