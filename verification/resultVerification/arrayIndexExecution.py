from definitions.ast.arrayIndexNode import ArrayIndexNode
from nodes.baseNodeHandler import BaseNodeHandler
from verification.resultVerification.jpypeValueTransformation import transform_to_jpype_value
from verification.resultVerification.resultDto import ResultDto


class ArrayIndexExecution(BaseNodeHandler[ResultDto]):
    def is_node(self, t: ResultDto):
        return isinstance(t.node, ArrayIndexNode)

    def handle(self, t: ResultDto):
        expression: ArrayIndexNode = t.node
        arr = t.result_verifier.evaluate(t.copy_with_other_node(expression.arr_expression))
        index = t.result_verifier.evaluate(t.copy_with_other_node(expression.index_expression))

        original = arr[index]
        return transform_to_jpype_value(original)
