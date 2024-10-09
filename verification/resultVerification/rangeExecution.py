from definitions.ast.RangeTreeNode import RangeTreeNode
from definitions.ast.quantifier.fullRangeTreeNode import FullRangeTreeNode
from verification.resultVerification.resultDto import ResultDto


class RangeExecution:
    def execute_range(self, range_: FullRangeTreeNode, ranges: list[RangeTreeNode], t: ResultDto):
        range_expr: RangeTreeNode = ranges[0]
        start = t.result_verifier.evaluate(t.copy_with_other_node(range_expr.start))
        if range_expr.start_operator == "<":
            start += 1

        end = t.result_verifier.evaluate(t.copy_with_other_node(range_expr.end))
        if range_expr.end_operator == "<=":
            end += 1

        for i in range(start, end):
            #result_copy = copy.deepcopy(result)
            #result_copy.parameters[range_expr.name] = i

            t.result_parameters.local_parameters[range_expr.name] = i

            if len(ranges) == 1:
                if range_.expr is not None:
                    if t.result_verifier.evaluate(t.copy_with_other_node(range_.expr)):
                        yield t

                    # if result_verifier.evaluate(result_copy, range_.expr):
                    #     yield result_copy
                else:
                    yield t
            else:
                for r in self.execute_range(range_, ranges[1:], t):
                    yield r
