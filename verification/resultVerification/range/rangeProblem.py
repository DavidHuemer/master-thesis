from z3 import Solver


class RangeProblem:
    def __init__(self):
        self.solver = Solver()
        self.solver.set("timeout", 1000)

    def add_constraint(self, constraint):
        self.solver.add(constraint)

    def check(self):
        return self.solver.check()

    def get_model(self):
        return self.solver.model()
