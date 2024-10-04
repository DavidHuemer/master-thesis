from z3 import Or, ArithRef, sat, ModelRef, ArrayRef, BoolRef

from definitions.evaluations.csp.parameters.cspParamHelperType import CSPParamHelperType
from definitions.evaluations.csp.parameters.jmlParameters import JmlParameters
from verification.csp.jmlSolver import JmlSolver


class JMLProblem:
    """
    Represents a JML problem that can be solved
    """

    def __init__(self, parameters: JmlParameters):
        self.parameters = parameters
        self.solver = JmlSolver()

    def add_constraint(self, constraint):
        """
        Adds a constraint to the problem.
        :param constraint: The constraint to add
        """
        self.solver.add_constraint(constraint)
        pass

    def push(self):
        """
        Pushes the current state of the solver.
        """
        self.solver.solver.push()

    def get_solver_solution(self):
        """
        Returns the solution of the current solver.
        :return: The solution of the current solver.
        """
        solution = self.solver.get_solution()
        return solution

    def get_distinct_constraint(self, solution, param):
        if isinstance(param, ArithRef) or isinstance(param, BoolRef):
            return param != solution[param]
        elif isinstance(param, ArrayRef):
            # Get length parameter
            length_param = self.parameters.csp_parameters.get_helper(str(param), CSPParamHelperType.LENGTH).value
            length = solution[length_param].as_long()

            if length == 0:
                return None

            or_expressions = [param[i] != solution.evaluate(param[i]).as_long() for i in range(length)]

            return Or(*or_expressions)

    def is_satisfiable(self):
        """
        Checks if the current constraints are satisfiable.
        :return: True if the constraints are satisfiable, False otherwise.
        """
        return self.solver.solver.check() == sat

    def pop_constraint(self):
        """
        Returns to the previous state of the solver.
        """
        self.solver.solver.pop()

    def add_solution_constraint(self, solution: ModelRef):
        """
        Adds an evaluated solution as a constraint to the problem.
        :param solution: The solution to add as a constraint.
        """
        if solution is None:
            return

        solution_params = [self.parameters.csp_parameters[str(var)].value for var in solution if self.parameters.csp_parameters.parameter_exists(str(var))]

        distinct_constraints = [self.get_distinct_constraint(solution, param) for param in solution_params]
        valid_constraints = [constraint for constraint in distinct_constraints if constraint is not None]

        if len(valid_constraints) == 0:
            return solution

        or_constraint = Or(*valid_constraints)
        self.add_constraint(or_constraint)
