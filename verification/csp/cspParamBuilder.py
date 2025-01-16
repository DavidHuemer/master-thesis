from z3 import Int, Array, IntSort, Real, Bool, RealSort, BoolSort, String, StringSort

from definitions.code.parameterExtractionInfo import ParameterExtractionInfo
from definitions.evaluations.csp.cspParameter import CSPParameter
from definitions.evaluations.csp.parameters.cspParamHelperType import CSPParamHelperType
from definitions.evaluations.csp.parameters.cspParameters import CSPParameters
from verification.csp.cspParamNameGenerator import find_csp_name


def build_csp_parameters(parameters: list[ParameterExtractionInfo]) -> CSPParameters:
    csp_parameters = CSPParameters()

    for param in parameters:
        csp_parameters.add_csp_parameter(get_csp_param_for_param(param))

    build_special_parameters(csp_parameters)
    build_helper_parameters(csp_parameters, parameters)

    return csp_parameters


def get_csp_param_for_param(param: ParameterExtractionInfo) -> CSPParameter:
    param_type_map = {
        "byte": Int,
        "short": Int,
        "int": Int,
        "long": Int,
        "float": Real,
        "double": Real,
        "boolean": Bool,
        "char": String,
        "String": String
    }

    if '[]' in param.parameter_type:
        return get_array_csp_param_for_param(param)

    if param.parameter_type in param_type_map:
        return CSPParameter(param.name, param_type_map[param.parameter_type](param.name), param.parameter_type)

    raise Exception(f"Parameter type {param.parameter_type} is not supported")


def get_array_csp_param_for_param(param: ParameterExtractionInfo) -> CSPParameter:
    array_param_type_map = {
        "byte[]": IntSort,
        "short[]": IntSort,
        "int[]": IntSort,
        "long[]": IntSort,
        "float[]": RealSort,
        "double[]": RealSort,
        "boolean[]": BoolSort,
        "char[]": StringSort,
        "String[]": StringSort
    }

    if param.parameter_type in array_param_type_map:
        return CSPParameter(param.name, Array(param.name, IntSort(), array_param_type_map[param.parameter_type]()),
                            param.parameter_type)

    raise Exception(f"Parameter type {param.parameter_type} is not supported")


def build_special_parameters(csp_parameters: CSPParameters):
    # Add is_null parameter
    is_null_name = find_csp_name(csp_parameters, "is_null")
    is_null_param = CSPParameter(is_null_name, Bool(is_null_name), "boolean", helper=True)

    csp_parameters.add_csp_parameter(is_null_param)
    csp_parameters.is_null_helper_param = is_null_param


def build_helper_parameters(csp_parameters: CSPParameters, parameters: list[ParameterExtractionInfo]):
    # Build helper parameters for each parameter
    for param in parameters:
        # Add is null
        is_null_name = find_csp_name(csp_parameters, f"{param.name}_is_null")
        is_null_param = CSPParameter(is_null_name, Bool(is_null_name), "boolean", helper=True)
        csp_parameters.add_helper_parameter(param.name, CSPParamHelperType.IS_NULL, is_null_param)

        # Add length for array parameters
        if "[]" in param.parameter_type:
            length_name = find_csp_name(csp_parameters, f"{param.name}_length")
            length_param = CSPParameter(length_name, Int(length_name), "int", helper=True)
            csp_parameters.add_helper_parameter(param.name, CSPParamHelperType.LENGTH, length_param)
