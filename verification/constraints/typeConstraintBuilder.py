from z3 import Length

from definitions import javaTypes
from definitions.evaluations.csp.cspParameter import CSPParameter
from definitions.evaluations.csp.jmlProblem import JMLProblem
from verification.constraints.arrayTypeConstraintBuilder import ArrayTypeConstraintBuilder
from verification.constraints.typeRanges import TypeRanges


class TypeConstraintBuilder:
    def __init__(self, type_ranges=TypeRanges(), array_type_constraint_builder=ArrayTypeConstraintBuilder()):
        self.type_ranges = type_ranges
        self.array_type_constraint_builder = array_type_constraint_builder

    def build_type_constraint(self, jml_problem: JMLProblem, parameter: CSPParameter):
        """
        Builds the type constraints for the given parameter.
        :param jml_problem: The JML problem that the constraints will be added to
        :param parameter: The parameter that the constraints will be built for
        """

        # Check if the parameter is a number
        if parameter.param_type in javaTypes.PRIMARY_ARITHMETIC_TYPES:
            self.add_number_constraints(jml_problem, parameter)

        # Check if the parameter is a string
        elif parameter.param_type in javaTypes.PRIMARY_TEXT_TYPES:
            self.add_text_constraints(jml_problem, parameter)

        # Check if the parameter is an array
        if parameter.is_array():
            self.array_type_constraint_builder.add_array_constraint(jml_problem, parameter)

    def add_number_constraints(self, jml_problem, parameter: CSPParameter):
        min_value, max_value = self.type_ranges.get_min_max_values(parameter.param_type)
        jml_problem.add_constraint(parameter.value >= min_value)
        jml_problem.add_constraint(parameter.value <= max_value)

    @staticmethod
    def add_text_constraints(jml_problem, parameter: CSPParameter):
        if parameter.param_type == javaTypes.CHAR_TYPE:
            jml_problem.add_constraint(Length(parameter.value) == 1)
