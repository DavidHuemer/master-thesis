from definitions.evaluations.BaseDto import BaseDto
from definitions.evaluations.csp.jmlProblem import JMLProblem
from definitions.evaluations.csp.parameters.constraintParameters import ConstraintParameters


class ConstraintsDto(BaseDto):
    def __init__(self, node,
                 jml_problem: JMLProblem,
                 constraint_parameters: ConstraintParameters):
        super().__init__(node=node)

        self.node = node
        self.jml_problem = jml_problem
        self.constraint_parameters = constraint_parameters

    def copy_with_other_node(self, node):
        return ConstraintsDto(
            node=node,
            jml_problem=self.jml_problem,
            constraint_parameters=self.constraint_parameters,
        )
