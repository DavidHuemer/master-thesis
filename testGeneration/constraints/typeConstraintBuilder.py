from z3 import Length, InRe, Re, Range, Star

from definitions import javaTypes
from definitions.evaluations.csp.cspParameter import CSPParameter
from definitions.evaluations.csp.jmlProblem import JMLProblem
from testGeneration.constraints.arrayTypeConstraintBuilder import add_array_constraint
from testGeneration.constraints.typeRanges import get_min_max_values


def build_type_constraint(jml_problem: JMLProblem, parameter: CSPParameter):
    """
    Builds the type constraints for the given parameter.
    :param jml_problem: The JML problem that the constraints will be added to
    :param parameter: The parameter that the constraints will be built for
    """

    # Check if the parameter is an array
    if parameter.is_array():
        add_array_constraint(jml_problem, parameter)

    # Check if the parameter is a number
    elif parameter.param_type in javaTypes.PRIMARY_ARITHMETIC_TYPES:
        add_number_constraints(jml_problem, parameter)

    # Check if the parameter is a string
    elif parameter.param_type in javaTypes.PRIMARY_TEXT_TYPES:
        add_text_constraints(jml_problem, parameter)


def add_number_constraints(jml_problem, parameter: CSPParameter):
    min_value, max_value = get_min_max_values(parameter.param_type)
    jml_problem.add_constraint(parameter.value >= min_value)
    jml_problem.add_constraint(parameter.value <= max_value)


def add_text_constraints(jml_problem, parameter: CSPParameter):
    if parameter.param_type == javaTypes.CHAR_TYPE:
        jml_problem.add_constraint(Length(parameter.value) == 1)

    allowed_chars = Range('0', '9') + Range('A', 'Z') + Range('a', 'z')
    jml_problem.add_constraint(InRe(parameter.value, Star(allowed_chars)))
