from z3 import Int, ForAll, Implies, And, Length

from definitions import javaTypes
from definitions.evaluations.csp.cspParameter import CSPParameter
from verification.constraints.typeRanges import TypeRanges


class ArrayTypeConstraintBuilder:
    def __init__(self, type_ranges=TypeRanges()):
        self.type_ranges = type_ranges

    def add_array_constraint(self, jml_problem, parameter: CSPParameter):
        length_name = f"{parameter.name}_length"
        length_parameter = jml_problem.parameters[length_name].value
        jml_problem.add_constraint(length_parameter >= 0)

        array_type = parameter.param_type[:-2]
        if array_type in javaTypes.PRIMARY_ARITHMETIC_TYPES:
            self.add_number_array_constraints(jml_problem, parameter, array_type, length_parameter)

        if array_type == javaTypes.CHAR_TYPE:
            self.add_char_array_constraints(jml_problem, parameter, length_parameter)

    def add_number_array_constraints(self, jml_problem, parameter, array_type, length_parameter):
        index = Int('index')
        min_value, max_value = self.type_ranges.get_min_max_values(array_type)
        jml_problem.add_constraint(
            ForAll(index, Implies(And(index >= 0, index < length_parameter),
                                  parameter.value[index] >= min_value))
        )
        jml_problem.add_constraint(
            ForAll(index, Implies(And(index >= 0, index < length_parameter),
                                  parameter.value[index] <= max_value))
        )

    @staticmethod
    def add_char_array_constraints(jml_problem, parameter, length_parameter):
        index = Int('index')
        jml_problem.add_constraint(
            ForAll(index, Implies(And(index >= 0, index < length_parameter),
                                  Length(parameter.value[index]) == 1))
        )
