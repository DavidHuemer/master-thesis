from definitions.evaluations.csp.cspParameter import CSPParameter
from definitions.evaluations.csp.jmlProblem import JMLProblem
from util.Singleton import Singleton
from verification.testConstraints.arrayTestConstraintGenerator import ArrayTestConstraintsGenerator
from verification.testConstraints.booleanTestConstraintGenerator import BooleanTestConstraintGenerator
from verification.testConstraints.charTestConstraints import CharTestConstraintGenerator
from verification.testConstraints.numericTestConstraintsGenerator import NumericTestConstraintsGenerator
from verification.testConstraints.stringTestConstraintGenerator import StringTestConstraintGenerator


class TestConstraintsGenerator(Singleton):
    """
    Helper class to build constraints for test case generation.
    The constraints are not extracted from the JML code, but are generated to increase the test coverage.
    """

    # TODO: Move into own service
    def __init__(self, numeric_test_constraint_generator=NumericTestConstraintsGenerator(),
                 boolean_test_constraint_generator=BooleanTestConstraintGenerator(),
                 array_test_constraints_generator=ArrayTestConstraintsGenerator(),
                 string_test_constraints_generator=StringTestConstraintGenerator(),
                 char_test_constraints_generator=CharTestConstraintGenerator()):
        self.boolean_test_constraint_generator = boolean_test_constraint_generator
        self.numeric_test_constraint_generator = numeric_test_constraint_generator
        self.array_test_constraints_generator = array_test_constraints_generator
        self.string_test_constraints_generator = string_test_constraints_generator
        self.char_test_constraints_generator = char_test_constraints_generator

    def get_test_constraints(self, jml_problem: JMLProblem, parameter: CSPParameter):
        if parameter.is_array():
            return self.array_test_constraints_generator.get_test_constraints(jml_problem, parameter)

        if self.numeric_test_constraint_generator.is_numeric(parameter):
            return self.numeric_test_constraint_generator.get_test_constraints(parameter)

        # TODO: Add support for char, string, and boolean types
        if self.boolean_test_constraint_generator.is_boolean(parameter):
            return self.boolean_test_constraint_generator.get_test_constraints(parameter)

        if self.string_test_constraints_generator.is_string(parameter):
            return self.string_test_constraints_generator.get_test_constraints(parameter)

        if self.char_test_constraints_generator.is_char(parameter):
            return self.char_test_constraints_generator.get_test_constraints(parameter)

        return []
