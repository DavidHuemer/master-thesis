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


param_type_map: dict[str, tuple[any, any]] = {
    "byte": (Int, IntSort),
    "short": (Int, IntSort),
    "int": (Int, IntSort),
    "long": (Int, IntSort),
    "float": (Real, RealSort),
    "double": (Real, RealSort),
    "boolean": (Bool, BoolSort),
    "char": (String, StringSort),
    "String": (String, StringSort)
}


def get_csp_param_for_param(param: ParameterExtractionInfo) -> CSPParameter:
    if param.variable_type in param_type_map:
        single_type, array_type = param_type_map[param.variable_type]
        if param.is_array():
            return CSPParameter(param.name, Array(param.name, IntSort(), array_type()), param.variable_type)
        return CSPParameter(param.name, single_type(param.name), param.variable_type)

    raise Exception(f"Parameter type {param.variable_type} is not supported")


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
        if param.is_array():
            length_name = find_csp_name(csp_parameters, f"{param.name}_length")
            length_param = CSPParameter(length_name, Int(length_name), "int", helper=True)
            csp_parameters.add_helper_parameter(param.name, CSPParamHelperType.LENGTH, length_param)
