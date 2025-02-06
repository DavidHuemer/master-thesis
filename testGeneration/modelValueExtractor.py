from jpype import JChar
from z3 import ModelRef

from definitions.evaluations.csp.parameters.cspParamHelperType import CSPParamHelperType
from definitions.evaluations.csp.parameters.cspParameters import CSPParameters


def get_value_of_param(csp_parameters: CSPParameters, param, model: ModelRef):
    csp_parameter = csp_parameters[str(param)]
    if csp_parameter.is_array():
        return get_array_value(csp_parameters, csp_parameter, param, model)

    wrapper = get_wrapper_for_type(csp_parameter.param_type)
    return wrapper(model[csp_parameter.value])


def get_array_value(csp_parameters: CSPParameters, csp_parameter, param, model):
    length_param = csp_parameters.get_helper(str(param), CSPParamHelperType.LENGTH).value
    length = model[length_param].as_long()

    wrapper = get_wrapper_for_type(csp_parameter.param_type)

    return [wrapper(model.evaluate(csp_parameter.value[i])) for i in range(length)]


def get_wrapper_for_type(param_type):
    if param_type == 'int' or param_type == 'long' or param_type == 'short' or param_type == 'byte':
        return arithmetic_arr_value
    elif param_type == 'float' or param_type == 'double':
        return lambda x: float(x.as_decimal(10))
    elif param_type == 'boolean':
        return lambda x: str(x) == 'True'
    elif param_type == 'char':
        return lambda x: JChar(x.as_string())
    elif param_type == 'String':
        return lambda x: x.as_string()
    return lambda x: x


def arithmetic_arr_value(value):
    return value.as_long()
