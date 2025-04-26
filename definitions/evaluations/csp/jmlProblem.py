import copy
import time

from z3 import Or, sat, And, Not

from definitions.evaluations.csp.cspParameter import CSPParameter
from definitions.parameters.Variables import Variables
from helper.logs.loggingHelper import log_info
from testGeneration.parameterModel import ParameterModel
from verification.csp.jmlSolver import JmlSolver


class JMLProblem:
    """
    Represents a JML problem that can be solved
    """

    def __init__(self, variables: Variables):
        self.variables = variables
        self.solver = JmlSolver()

    def add_constraint(self, constraint):
        """
        Adds a constraint to the problem.
        :param constraint: The constraint to add
        """
        self.solver.add_constraint(constraint)

    def push(self):
        """
        Pushes the current state of the solver.
        """
        self.solver.solver.push()

    def get_solver_solution(self) -> Variables | None:
        """
        Returns the solution of the current solver.
        :return: The solution of the current solver.
        """

        model = self.solver.get_solution()

        if model is None:
            return None

        variables_copy = copy.copy(self.variables)

        variables_copy.method_call_parameters.evaluate(model) if model is not None else None
        return variables_copy

    @staticmethod
    def get_distinct_constraints(csp_param: CSPParameter, value):
        if csp_param.is_array() and value is not None:
            or_expressions = [csp_param.value[i] != value[i] for i in range(len(value))]
            or_expressions.append(csp_param.length_param != len(value))
            return Or(*or_expressions)

        if value is None:
            return csp_param.is_null_param != True

        return csp_param != value

    def is_satisfiable(self):
        """
        Checks if the current constraints are satisfiable.
        :return: True if the constraints are satisfiable, False otherwise.
        """
        return self.solver.solver.check() == sat

    def pop(self):
        """
        Returns to the previous state of the solver.
        """
        self.solver.solver.pop()

    def add_solution_constraint(self, variables: Variables):
        """
        Adds an evaluated solution as a constraint to the problem.
        :param variables: The solution to add as a constraint.
        """

        if variables is None:
            return

        constraints = variables.method_call_parameters.get_constraints()
        if len(constraints) == 0:
            return

        and_constraint = And(*constraints)
        self.add_constraint(Not(and_constraint))
        #
        #
        #
        # distinct_constraints = [
        #     self.get_distinct_constraints(self.variables.csp_parameters[key],
        #                                   variables.parameter_dict[key])
        #     for key in variables.parameter_dict
        # ]
        #
        # valid_constraints = [constraint for constraint in distinct_constraints if constraint is not None]
        #
        # if len(valid_constraints) == 0:
        #     return
        # elif len(valid_constraints) == 1:
        #     self.add_constraint(valid_constraints[0])
        #     return
        #
        # or_constraint = Or(*valid_constraints)
        # self.add_constraint(or_constraint)
