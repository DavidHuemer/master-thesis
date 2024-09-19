from definitions.ast.RangeTreeNode import RangeTreeNode
from definitions.parser.parserResult import ParserResult
from parser.generated import JMLParser


class QuantifierSimplifier:
    @staticmethod
    def get_type_declarations(types: JMLParser.JMLParser.Type_declarationsContext):
        variable_names = []

        for type_declaration in types.children:
            # Type is the first child of the type declaration
            t = type_declaration.children[0].getText()

            # All other children are variable names
            for i in range(1, len(type_declaration.children)):
                variable_names.append((t, type_declaration.children[i].getText()))

        return variable_names

    @staticmethod
    def get_ranges(range_expression: JMLParser.JMLParser.Range_expressionContext, parser_result: ParserResult,
                   jml_simplifier):
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
