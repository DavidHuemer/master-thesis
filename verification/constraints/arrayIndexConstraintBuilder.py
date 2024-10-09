from definitions.ast.arrayIndexNode import ArrayIndexNode
from nodes.baseNodeHandler import BaseNodeHandler
from verification.constraints.constraintsDto import ConstraintsDto


class ArrayIndexConstraintBuilder(BaseNodeHandler[ConstraintsDto]):

    def is_node(self, t: ConstraintsDto):
        return isinstance(t.node, ArrayIndexNode)

    def handle(self, t: ConstraintsDto):
        expression: ArrayIndexNode = t.node
        array_expr = t.constraint_builder.evaluate(t.copy_with_other_node(expression.arr_expression))
        index_expr = t.constraint_builder.evaluate(t.copy_with_other_node(expression.index_expression))
        return array_expr[index_expr]
