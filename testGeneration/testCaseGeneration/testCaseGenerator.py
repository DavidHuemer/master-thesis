import time

from codetiming import Timer
from dependency_injector.wiring import Provide, inject
from z3 import And

from definitions.evaluations.csp.jmlProblem import JMLProblem
from definitions.verification.testCase import TestCase
from helper.logs.loggingHelper import log_info
from testGeneration.testCaseGeneration.testCaseBuilder import build_test_case
from testGeneration.testCaseGeneration.testCaseGenerationContainer import TestCaseGenerationContainer
from verification.testConstraints.testConstraintsGenerator import TestConstraintsGenerator

generate_for_parameter_timer = Timer(name="generate_for_parameter", logger=None)


def generate_test_cases(jml_problem: JMLProblem):
    return generate_solver_test_cases(jml_problem)


def generate_solver_test_cases(jml_problem: JMLProblem) -> list[TestCase]:
    # All real parameters (that are not helper)
    real_parameters = jml_problem.parameters.csp_parameters.get_actual_parameters()
    log_info("Generating for parameters")

    start_time = time.time()
    test_cases = generate_for_parameters(jml_problem, real_parameters, [])
    end_time = time.time()
    elapsed_time = end_time - start_time
    log_info(f"Generated {len(test_cases)} test cases in {elapsed_time} seconds")
    return test_cases


@inject
def generate_for_parameters(jml_problem: JMLProblem, parameters, actions,
                            test_constraint_generator: TestConstraintsGenerator = Provide[
                                TestCaseGenerationContainer.test_constraint_generator]) -> list[TestCase]:
    parameter = parameters[0]
    test_cases: list[TestCase] = []

    for param_constraint in test_constraint_generator.get_test_constraints(jml_problem, parameter):
        working_actions = actions + [param_constraint]

        if len(parameters) == 1:
            test_case = generate_for_parameter_constraints(jml_problem, working_actions)
            if test_case is not None:
                test_cases.append(test_case)
        else:
            new_arr = generate_for_parameters(jml_problem, parameters[1:], working_actions)
            test_cases.extend(new_arr)

    return test_cases


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
