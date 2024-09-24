from z3 import Int, Array, IntSort, Real, Bool, RealSort, BoolSort

from definitions.code.parameterExtractionInfo import ParameterExtractionInfo
from definitions.evaluations.csp.cspParameter import CSPParameter
from definitions.javaMethod import JavaMethod


class CSPParameterBuilder:
    """
    Class that is used for building parameters that are needed for the solver
    """

    def build_parameters(self, method_info: JavaMethod) -> dict[str, CSPParameter]:
        csp_params: dict[str, CSPParameter] = dict()

        for param in method_info.parameters_list:
            csp_params[param.name] = self.get_csp_param_for_param(param)

            # Add is_null parameter for each parameter
            is_null_name = f"{param.name}_is_null"
            csp_params[is_null_name] = CSPParameter(is_null_name, Bool(is_null_name), "boolean", helper=True)

            # For array parameters add the length of the array
            # Check if param includes []
            if "[]" in param.parameter_type:
                csp_params[param.name + "_length"] = CSPParameter(param.name + "_length",
                                                                  Int(param.name + "_length"), "int", helper=True)

        return csp_params

    def get_csp_param_for_param(self, param: ParameterExtractionInfo) -> CSPParameter:
        if '[]' in param.parameter_type:
            return self.get_array_csp_param_for_param(param)

        if param.parameter_type == "int":
            return CSPParameter(param.name, Int(param.name), param.parameter_type)

        if param.parameter_type == "long":
            return CSPParameter(param.name, Int(param.name), param.parameter_type)

        if param.parameter_type == "float":
            return CSPParameter(param.name, Real(param.name), param.parameter_type)

        if param.parameter_type == "double":
            return CSPParameter(param.name, Real(param.name), param.parameter_type)

        if param.parameter_type == "boolean":
            return CSPParameter(param.name, Bool(param.name), param.parameter_type)

        raise Exception(f"Parameter type {param.parameter_type} is not supported")

    @staticmethod
    def get_array_csp_param_for_param(param: ParameterExtractionInfo) -> CSPParameter:
        if param.parameter_type == "int[]":
            return CSPParameter(param.name, Array(param.name, IntSort(), IntSort()), param.parameter_type)

        if param.parameter_type == "long[]":
            return CSPParameter(param.name, Array(param.name, IntSort(), IntSort()), param.parameter_type)

        if param.parameter_type == "float[]":
            return CSPParameter(param.name, Array(param.name, IntSort(), RealSort()), param.parameter_type)

        if param.parameter_type == "double[]":
            return CSPParameter(param.name, Array(param.name, IntSort(), RealSort()), param.parameter_type)

        if param.parameter_type == "boolean[]":
            return CSPParameter(param.name, Array(param.name, IntSort(), BoolSort()), param.parameter_type)

        raise Exception(f"Parameter type {param.parameter_type} is not supported")
