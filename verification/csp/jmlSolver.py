from z3 import Solver, sat

from verification.csp.cspProblem import CSPProblem


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

    def add_constraint(self, constraint):
        super().add_constraint(constraint)
        self.solver.add(constraint)

    def get_solution(self):
        if self.solver.check() != sat:
            return None

        return self.solver.model()
