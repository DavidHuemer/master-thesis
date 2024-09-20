from definitions.evaluations.csp.cspParameter import CSPParameter
from definitions.evaluations.csp.jmlProblem import JMLProblem
from verification.testConstraints.arrayTestConstraintGenerator import ArrayTestConstraintsGenerator
from verification.testConstraints.numericTestConstraintsGenerator import NumericTestConstraintsGenerator


class TestConstraintsGenerator:
    """
    Helper class to build constraints for test case generation.
    The constraints are not extracted from the JML code, but are generated to increase the test coverage.
    """

    def __init__(self, numeric_test_constraint_generator=NumericTestConstraintsGenerator(),
                 array_test_constraints_generator=ArrayTestConstraintsGenerator()):
        self.numeric_test_constraint_generator = numeric_test_constraint_generator
        self.array_test_constraints_generator = array_test_constraints_generator

    def get_test_constraints(self, jml_problem: JMLProblem, parameter: CSPParameter):
        if self.numeric_test_constraint_generator.is_numeric(parameter):
            return self.numeric_test_constraint_generator.get_test_constraints(parameter)

        if parameter.is_array():
            return self.array_test_constraints_generator.get_test_constraints(jml_problem, parameter)

        return []
