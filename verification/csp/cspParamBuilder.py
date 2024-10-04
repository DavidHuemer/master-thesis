from z3 import Int, Array, IntSort, Real, Bool, RealSort, BoolSort, String, StringSort

from definitions.code.parameterExtractionInfo import ParameterExtractionInfo
from definitions.evaluations.csp.cspParameter import CSPParameter
from definitions.evaluations.csp.parameters.cspParamHelperType import CSPParamHelperType
from definitions.evaluations.csp.parameters.cspParameters import CSPParameters
from verification.csp.cspParamNameGenerator import CspParamNameGenerator


class CSPParameterBuilder:
    """
    Class that is used for building parameters that are needed for the solver
    """

    def __init__(self, csp_param_name_generator=CspParamNameGenerator()):
        self.csp_param_name_generator = csp_param_name_generator

    def build_csp_parameters(self, parameters: list[ParameterExtractionInfo]) -> CSPParameters:
        csp_parameters = CSPParameters()

        # Add normal parameters
        for param in parameters:
            csp_parameters.add_csp_parameter(self.get_csp_param_for_param(param))

        # Add special parameters
        self.build_special_parameters(csp_parameters)

        # Add helper parameters
        self.build_helper_parameters(csp_parameters, parameters)
        return csp_parameters

    def build_special_parameters(self, csp_parameters: CSPParameters):
        # Add is_null parameter
        is_null_name = self.csp_param_name_generator.find_name(csp_parameters, "is_null")
        is_null_param = CSPParameter(is_null_name, Bool(is_null_name), "boolean", helper=True)

        csp_parameters.add_csp_parameter(is_null_param)
        csp_parameters.is_null_helper_param = is_null_param

    def build_helper_parameters(self, csp_parameters: CSPParameters, parameters: list[ParameterExtractionInfo]):
        # Build helper parameters for each parameter
        for param in parameters:
            # Add is null
            is_null_name = self.csp_param_name_generator.find_name(csp_parameters, f"{param.name}_is_null")
            is_null_param = CSPParameter(is_null_name, Bool(is_null_name), "boolean", helper=True)
            csp_parameters.add_helper_parameter(param.name, CSPParamHelperType.IS_NULL, is_null_param)

            # Add length for array parameters
            if "[]" in param.parameter_type:
                length_name = self.csp_param_name_generator.find_name(csp_parameters, f"{param.name}_length")
                length_param = CSPParameter(length_name, Int(length_name), "int", helper=True)
                csp_parameters.add_helper_parameter(param.name, CSPParamHelperType.LENGTH, length_param)

    # for param in parameters:

    def get_csp_param_for_param(self, param: ParameterExtractionInfo) -> CSPParameter:
        if '[]' in param.parameter_type:
            return self.get_array_csp_param_for_param(param)

        if param.parameter_type == "byte":
            return CSPParameter(param.name, Int(param.name), param.parameter_type)
        elif param.parameter_type == "short":
            return CSPParameter(param.name, Int(param.name), param.parameter_type)
        elif param.parameter_type == "int":
            return CSPParameter(param.name, Int(param.name), param.parameter_type)
        elif param.parameter_type == "long":
            return CSPParameter(param.name, Int(param.name), param.parameter_type)
        elif param.parameter_type == "float":
            return CSPParameter(param.name, Real(param.name), param.parameter_type)
        elif param.parameter_type == "double":
            return CSPParameter(param.name, Real(param.name), param.parameter_type)
        elif param.parameter_type == "boolean":
            return CSPParameter(param.name, Bool(param.name), param.parameter_type)
        elif param.parameter_type == "char":
            return CSPParameter(param.name, String(param.name), param.parameter_type)
        elif param.parameter_type == "String":
            return CSPParameter(param.name, String(param.name), param.parameter_type)

        raise Exception(f"Parameter type {param.parameter_type} is not supported")

    @staticmethod
    def get_array_csp_param_for_param(param: ParameterExtractionInfo) -> CSPParameter:
        if param.parameter_type == "byte[]":
            return CSPParameter(param.name, Array(param.name, IntSort(), IntSort()), param.parameter_type)
        elif param.parameter_type == "short[]":
            return CSPParameter(param.name, Array(param.name, IntSort(), IntSort()), param.parameter_type)
        elif param.parameter_type == "int[]":
            return CSPParameter(param.name, Array(param.name, IntSort(), IntSort()), param.parameter_type)
        elif param.parameter_type == "long[]":
            return CSPParameter(param.name, Array(param.name, IntSort(), IntSort()), param.parameter_type)
        elif param.parameter_type == "float[]":
            return CSPParameter(param.name, Array(param.name, IntSort(), RealSort()), param.parameter_type)
        elif param.parameter_type == "double[]":
            return CSPParameter(param.name, Array(param.name, IntSort(), RealSort()), param.parameter_type)
        elif param.parameter_type == "boolean[]":
            return CSPParameter(param.name, Array(param.name, IntSort(), BoolSort()), param.parameter_type)
        elif param.parameter_type == "char[]":
            return CSPParameter(param.name, Array(param.name, IntSort(), StringSort()), param.parameter_type)
        elif param.parameter_type == "String[]":
            return CSPParameter(param.name, Array(param.name, IntSort(), StringSort()), param.parameter_type)

        raise Exception(f"Parameter type {param.parameter_type} is not supported")
