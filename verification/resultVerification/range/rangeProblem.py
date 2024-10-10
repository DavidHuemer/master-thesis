from z3 import Solver


class RangeProblem:
    def __init__(self):
        self.solver = Solver()

    def add_constraint(self, constraint):
        self.solver.add(constraint)

    def check(self):
        return self.solver.check()

    def get_model(self):
        return self.solver.model()
