from z3 import Or, sat

from definitions.evaluations.csp.cspParameter import CSPParameter
from definitions.evaluations.csp.parameters.jmlParameters import JmlParameters
from testGeneration.parameterModel import ParameterModel
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

    def push(self):
        """
        Pushes the current state of the solver.
        """
        self.solver.solver.push()

    def get_solver_solution(self) -> ParameterModel | None:
        """
        Returns the solution of the current solver.
        :return: The solution of the current solver.
        """
        model = self.solver.get_solution()
        return ParameterModel(model, self.parameters.csp_parameters) if model is not None else None

    @staticmethod
    def get_distinct_constraints(csp_param: CSPParameter, value):
        if csp_param.is_array():
            or_expressions = [csp_param.value[i] != value[i] for i in range(len(value))]
            or_expressions.append(csp_param.length_param != len(value))
            return Or(*or_expressions)

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

    def add_solution_constraint(self, parameter_model: ParameterModel):
        """
        Adds an evaluated solution as a constraint to the problem.
        :param parameter_model: The solution to add as a constraint.
        """

        if parameter_model is None:
            return

        distinct_constraints = [
            self.get_distinct_constraints(self.parameters.csp_parameters[key],
                                          parameter_model.parameter_dict[key])
            for key in parameter_model.parameter_dict
        ]

        valid_constraints = [constraint for constraint in distinct_constraints if constraint is not None]

        if len(valid_constraints) == 0:
            return
        elif len(valid_constraints) == 1:
            self.add_constraint(valid_constraints[0])
            return

        or_constraint = Or(*valid_constraints)
        self.add_constraint(or_constraint)
