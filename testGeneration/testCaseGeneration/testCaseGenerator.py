from itertools import product

from codetiming import Timer
from dependency_injector.wiring import inject
from z3 import And

from definitions.evaluations.csp.jmlProblem import JMLProblem
from definitions.verification.testCase import TestCase
from helper.logs.loggingHelper import log_info
from testGeneration.testCaseGeneration.testCaseBuilder import build_test_case
from verification.testConstraints.testConstraintsGenerator import TestConstraintsGenerator

generate_for_parameter_timer = Timer(name="generate_for_parameter", logger=None)


def generate_test_cases(jml_problem: JMLProblem):
    return generate_solver_test_cases(jml_problem)


def generate_solver_test_cases(jml_problem: JMLProblem) -> list[TestCase]:
    # All real parameters (that are not helper)
    real_parameters = jml_problem.parameters.csp_parameters.get_actual_parameters()
    log_info("Generating for parameters")

    return [result for constraint in get_constraints(jml_problem, real_parameters)
            if (result := generate_for_parameter_constraints(jml_problem, constraint)) is not None]


def get_combinations(parameters):
    return product(*parameters)


@inject
def get_constraints(jml_problem: JMLProblem, parameters):
    new_params = [TestConstraintsGenerator().get_test_constraints(jml_problem, element) for element in parameters]
    return get_combinations(new_params)


@generate_for_parameter_timer
def generate_for_parameter_constraints(jml_problem: JMLProblem, constraints):
    singular_constraint = And(*constraints) if len(constraints) > 1 else constraints[0]
    jml_problem.push()
    jml_problem.add_constraint(singular_constraint)

    solution = jml_problem.get_solver_solution()
    jml_problem.pop_constraint()

    if solution is not None:
        jml_problem.add_solution_constraint(solution)
        return build_test_case(jml_problem, solution)

    return None
