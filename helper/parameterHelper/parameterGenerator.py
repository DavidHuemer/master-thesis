import jpype

from definitions.code.parameterExtractionInfo import ParameterExtractionInfo
from definitions.parameters.parameter import Parameter
from definitions.parameters.parameterState import ParameterState
from verification.csp.cspParamBuilder import build_csp_param


def get_initial_parameter(java_type: str, name: str, dimension: int = 0) -> Parameter:
    csp = build_csp_param(java_type, name, dimension)

    old = ParameterState(csp_parameter=csp)
    return Parameter(old, None)


def get_parameter_by_parameter_extraction_info(parameter_extraction_info: ParameterExtractionInfo):
    return get_initial_parameter(parameter_extraction_info.variable_type,
                                 parameter_extraction_info.name,
                                 parameter_extraction_info.dimension)


def get_parameters_by_parameter_extraction_infos(parameter_extraction_infos: list[ParameterExtractionInfo]):
    return [get_parameter_by_parameter_extraction_info(parameter_extraction_info)
            for parameter_extraction_info in parameter_extraction_infos]
