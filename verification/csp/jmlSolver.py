from codetiming import Timer
from z3 import Solver, sat, ModelRef

from testGeneration.parameterModel import ParameterModel
from verification.csp.cspProblem import CSPProblem

add_constraint_timer = Timer(name="add_constraint", logger=None)
solution_generation_timer = Timer(name="solution_generation", logger=None)


class JmlSolver(CSPProblem):
    """
    Class that represents a CSP solver for JML
    """

    def __init__(self):
        """
        Constructor for the JmlSolver class
        """
        super().__init__()
        self.solver = Solver()

    @add_constraint_timer
    def add_constraint(self, constraint):
        super().add_constraint(constraint)
        self.solver.add(constraint)

    @solution_generation_timer
    def get_solution(self) -> ModelRef | None:
        if self.solver.check() != sat:
            return None

        return self.solver.model()
