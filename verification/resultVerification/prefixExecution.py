from definitions.ast.prefixNode import PrefixNode
from nodes.baseNodeHandler import BaseNodeHandler
from verification.resultVerification.resultDto import ResultDto


class PrefixExecution(BaseNodeHandler[ResultDto]):

    def is_node(self, t: ResultDto):
        return isinstance(t.node, PrefixNode)

    def handle(self, t: ResultDto):
        expression: PrefixNode = t.node

        evaluated_expr = t.result_verifier.evaluate(t.copy_with_other_node(expression.expr))

        if expression.prefix == '++':
            return evaluated_expr + 1
        elif expression.prefix == '--':
            return evaluated_expr - 1
        elif expression.prefix == '!':
            return not evaluated_expr
        elif expression.prefix == '-':
            return -evaluated_expr
        elif expression.prefix == '+':
            return evaluated_expr
        elif expression.prefix == '~':
            return ~evaluated_expr
