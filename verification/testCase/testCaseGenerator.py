from z3 import And

from definitions.evaluations.csp.jmlProblem import JMLProblem
from definitions.verification.testCase import TestCase
from verification.testCase.testCaseBuilder import TestCaseBuilder
from verification.testConstraints.testConstraintsGenerator import TestConstraintsGenerator


class TestCasesGenerator:
    def __init__(self, test_constraint_generator=TestConstraintsGenerator(),
                 test_case_builder=TestCaseBuilder()):
        self.test_constraints_generator = test_constraint_generator
        self.test_case_builder = test_case_builder

    def generate(self, jml_problem: JMLProblem) -> list[TestCase]:
        solver_test_cases = self.generate_solver_test_cases(jml_problem)
        return solver_test_cases

    def generate_solver_test_cases(self, jml_problem: JMLProblem) -> list[TestCase]:

        # All real parameters (that are not helper)
        real_parameters = [jml_problem.parameters[param] for param in jml_problem.parameters if
                           not jml_problem.parameters[param].is_helper]
        test_cases = self.generate_for_parameters(jml_problem, real_parameters, [])
        return test_cases

    def generate_for_parameters(self, jml_problem: JMLProblem, parameters, actions) -> list[TestCase]:
        parameter = parameters[0]
        test_cases: list[TestCase] = []

        for param_constraint in self.test_constraints_generator.get_test_constraints(jml_problem, parameter):
            working_actions = actions + [param_constraint]

            if len(parameters) == 1:
                test_case = self.generate_for_parameter_constraints(jml_problem, working_actions)
                if test_case is not None:
                    test_cases.append(test_case)
            else:
                new_arr = self.generate_for_parameters(jml_problem, parameters[1:], working_actions)
                test_cases.extend(new_arr)

        return test_cases

    def generate_for_parameter_constraints(self, jml_problem: JMLProblem, constraints):
        singular_constraint = And(*constraints)
        jml_problem.push()
        jml_problem.add_constraint(singular_constraint)
        solution = jml_problem.get_solver_solution()
        jml_problem.pop_constraint()

        if solution is not None:
            jml_problem.add_solution_constraint(solution)
            return self.test_case_builder.build_test_case(jml_problem, solution)

        return None
