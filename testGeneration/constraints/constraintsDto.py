from definitions.ast.astTreeNode import AstTreeNode
from definitions.evaluations.BaseDto import BaseDto
from definitions.evaluations.csp.jmlProblem import JMLProblem


class ConstraintsDto(BaseDto):
    def __init__(self, node: AstTreeNode,
                 jml_problem: JMLProblem):
        super().__init__(node=node)

        self.node = node
        self.jml_problem = jml_problem

    def copy_with_other_node(self, node):
        return ConstraintsDto(
            node=node,
            jml_problem=self.jml_problem,
        )
