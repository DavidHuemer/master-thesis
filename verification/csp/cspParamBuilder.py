from z3 import Int, Array, IntSort, Real, Bool, RealSort, BoolSort, String, StringSort

from definitions.code.parameterExtractionInfo import ParameterExtractionInfo
from definitions.evaluations.csp.cspParameter import CSPParameter
from definitions.evaluations.csp.parameters.cspParameters import CSPParameters


def build_csp_parameters(parameters: list[ParameterExtractionInfo]) -> CSPParameters:
    csp_parameters = CSPParameters()

    for param in parameters:
        csp_parameters.add_csp_parameter(get_csp_param_for_param(param))

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
