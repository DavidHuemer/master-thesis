import copy

from definitions.ast.RangeTreeNode import RangeTreeNode
from definitions.codeExecution.result.executionResult import ExecutionResult


class RangeExecution:
    def execute_range(self, ranges: list[RangeTreeNode], result: ExecutionResult, result_verifier):
        range_expr: RangeTreeNode = ranges[0]
        start = result_verifier.evaluate(result, range_expr.start)
        if range_expr.start_operator == "<":
            start += 1

        end = result_verifier.evaluate(result, range_expr.end)
        if range_expr.end_operator == "<=":
            end += 1

        for i in range(start, end):
            result_copy = copy.deepcopy(result)
            result_copy.parameters[range_expr.name] = i

            if len(ranges) == 1:
                yield result_copy
            else:
                for r in self.execute_range(ranges[1:], result_copy, result_verifier):
                    yield r
