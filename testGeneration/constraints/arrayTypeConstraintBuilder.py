import uuid

from z3 import Int, ForAll, Implies, And, Length

from definitions import javaTypes
from definitions.evaluations.csp.cspParameter import CSPParameter
from definitions.evaluations.csp.jmlProblem import JMLProblem
from definitions.evaluations.csp.parameters.cspParamHelperType import CSPParamHelperType
from testGeneration.constraints.typeRanges import get_min_max_values


def add_array_constraint(jml_problem: JMLProblem, parameter: CSPParameter):
    length_parameter = parameter.length_param
    jml_problem.add_constraint(length_parameter >= 0)

    array_type = parameter.param_type
    if array_type in javaTypes.PRIMARY_ARITHMETIC_TYPES:
        add_number_array_constraints(jml_problem, parameter, array_type, length_parameter)

    if array_type == javaTypes.CHAR_TYPE:
        add_char_array_constraints(jml_problem, parameter, length_parameter)


def add_number_array_constraints(jml_problem, parameter, array_type, length_parameter):
    index = Int(f"index_{uuid.uuid4()}")
    min_value, max_value = get_min_max_values(array_type)
    jml_problem.add_constraint(
        ForAll(index, Implies(And(index >= 0, index < length_parameter),
                              And(parameter.value[index] >= min_value, parameter.value[index] <= max_value)))
    )


def add_char_array_constraints(jml_problem, parameter, length_parameter):
    index = Int('index')
    jml_problem.add_constraint(
        ForAll(index, Implies(And(index >= 0, index < length_parameter),
                              Length(parameter.value[index]) == 1))
    )
