from itertools import product

from z3 import And

from definitions.evaluations.csp.jmlProblem import JMLProblem
from definitions.parameters.Variables import Variables
from definitions.parameters.parameters import Parameters
from helper.logs.loggingHelper import log_info
from verification.testConstraints.testConstraintsGenerator import TestConstraintsGenerator
import time


def generate_test_cases(jml_problem: JMLProblem) -> list[Variables]:
    log_info("Generating test cases")
    return generate_solver_test_cases(jml_problem)


def generate_solver_test_cases(jml_problem: JMLProblem) -> list[Variables]:
    # All real parameters (that are not helper)

    return [result for constraint in get_constraints(jml_problem, jml_problem.variables.method_call_parameters)
            if (result := generate_test_case_by_constraints(jml_problem, constraint)) is not None]


def get_combinations(parameters):
    return product(*parameters)


def get_constraints(jml_problem: JMLProblem, parameters: Parameters):
    constraints_per_parameter = [
        TestConstraintsGenerator().get_test_constraints(jml_problem, parameter.get_state(use_old=True).csp_parameter)
        for parameter in parameters]
    return get_combinations(constraints_per_parameter)


def generate_test_case_by_constraints(jml_problem: JMLProblem, constraints) -> Variables | None:
    singular_constraint = And(*constraints) if len(constraints) > 1 else constraints[0]
    jml_problem.push()
    jml_problem.add_constraint(singular_constraint)

    current_millis = time.time()
    solution_variables = jml_problem.get_solver_solution()
    after_millis = time.time()

    #log_info(f"Solver took {after_millis - current_millis} seconds to find a solution")

    jml_problem.pop()

    if solution_variables is not None:
        jml_problem.add_solution_constraint(solution_variables)
        return solution_variables

    return None
