from z3 import Int, ForAll

from definitions import javaTypes
from definitions.evaluations.csp.cspParameter import CSPParameter
from definitions.evaluations.csp.jmlProblem import JMLProblem


class TypeConstraintBuilder:
    def build_type_constraint(self, jml_problem: JMLProblem, parameter: CSPParameter):
        """
        Builds the type constraints for the given parameter.
        :param jml_problem: The JML problem that the constraints will be added to
        :param parameter: The parameter that the constraints will be built for
        """

        # Check if the parameter is a number
        if parameter.param_type in javaTypes.PRIMARY_ARITHMETIC_TYPES:
            self.add_number_constraints(jml_problem, parameter)

        # Check if the parameter is an array
        if parameter.is_array():
            self.add_array_constraints(jml_problem, parameter)

    def add_number_constraints(self, jml_problem, parameter):
        min_value, max_value = self.get_min_max_values(parameter.param_type)
        jml_problem.add_constraint(parameter.value >= min_value)
        jml_problem.add_constraint(parameter.value <= max_value)

    @staticmethod
    def get_min_max_values(parameter_type: str):
        """
        Returns the minimum and maximum values for the given parameter type.
        :param parameter_type:
        :return:
        """
        if parameter_type == javaTypes.INT_TYPE:
            return -10000, 10000
            #return -(2 ** 31 - 1), 2 ** 31 - 1

        if parameter_type == javaTypes.LONG_TYPE:
            return -(2 ** 63 - 1), 2 ** 63 - 1

        if parameter_type == javaTypes.FLOAT_TYPE:
            return -3.4028235e38, 3.4028235e38

        if parameter_type == javaTypes.DOUBLE_TYPE:
            return -1.7976931348623157e308, 1.7976931348623157e308

        raise Exception(f"Cannot get min/max values for parameter type {parameter_type}.")

    def add_array_constraints(self, jml_problem, parameter):
        length_name = f"{parameter.name}_length"
        length_parameter = jml_problem.parameters[length_name].value

        jml_problem.add_constraint(length_parameter >= 0)

        array_type = parameter.param_type[:-2]

        if array_type not in javaTypes.PRIMARY_ARITHMETIC_TYPES:
            return

        index_name = f"{parameter.name}_index"
        index_parameter = Int(index_name)

        min_value, max_value = self.get_min_max_values(array_type)
        jml_problem.add_constraint(ForAll(index_parameter, parameter.value[index_parameter] >= min_value))
        jml_problem.add_constraint(ForAll(index_parameter, parameter.value[index_parameter] <= max_value))
