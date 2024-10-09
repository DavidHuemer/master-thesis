from definitions.evaluations.csp.jmlProblem import JMLProblem
from definitions.evaluations.csp.parameters.constraintParameters import ConstraintParameters


class ConstraintsDto:
    def __init__(self, node,
                 jml_problem: JMLProblem,
                 constraint_parameters: ConstraintParameters,
                 constraint_builder):
        from verification.constraints.expressionConstraintBuilder import ExpressionConstraintBuilder

        self.node = node
        self.jml_problem = jml_problem
        self.constraint_parameters = constraint_parameters
        self.constraint_builder: ExpressionConstraintBuilder = constraint_builder

    def copy_with_other_node(self, node):
        return ConstraintsDto(
            node=node,
            jml_problem=self.jml_problem,
            constraint_parameters=self.constraint_parameters,
            constraint_builder=self.constraint_builder
        )
