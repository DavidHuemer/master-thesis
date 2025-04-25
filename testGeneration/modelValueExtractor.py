from jpype import JChar
from z3 import ModelRef

from definitions.evaluations.csp.cspParameter import CSPParameter
from definitions.evaluations.csp.parameters.cspParameters import CSPParameters
from definitions.parameters.parameterValue import ParameterValue
from helper.parameterHelper.parameterValueGenerator import get_parameter_value_by_python


def get_parameter_value(csp_parameter: CSPParameter, model: ModelRef, func_decl_dict) -> ParameterValue:
    is_null_csp_name = str(csp_parameter.is_null_param)
    is_null_func_decl = func_decl_dict.get(is_null_csp_name)

    if is_null_func_decl is not None:
        is_null = model[is_null_func_decl]
        if is_null:
            return get_parameter_value_by_python(None, csp_parameter.param_type)

    csp_name = str(csp_parameter.value)
    csp_func_decl = func_decl_dict.get(csp_name)
    value = model[csp_func_decl]

    wrapper = get_wrapper_for_type(csp_parameter.param_type)

    if csp_parameter.is_array():
        length_param_name = str(csp_parameter.length_param)
        length_func_decl = func_decl_dict.get(length_param_name)
        length = model[length_func_decl].as_long()
        lst = [wrapper(model.evaluate(csp_parameter.value[i])) for i in range(length)]
        return get_parameter_value_by_python(lst, csp_parameter.param_type)
    else:
        return get_parameter_value_by_python(wrapper(value), csp_parameter.param_type)


def get_value_of_param(csp_parameters: CSPParameters, param, model: ModelRef):
    csp_parameter = csp_parameters[str(param)]
    if csp_parameter.is_array():
        return get_array_value(csp_parameters, csp_parameter, param, model)

    wrapper = get_wrapper_for_type(csp_parameter.param_type)
    try:
        return wrapper(model.evaluate(csp_parameter.value))
    except Exception as e:
        return None


def get_array_value(csp_parameters: CSPParameters, csp_parameter, param, model):
    length_param = csp_parameters[str(param)].length_param
    length = model[length_param].as_long()

    wrapper = get_wrapper_for_type(csp_parameter.param_type)

    return [wrapper(model.evaluate(csp_parameter.value[i])) for i in range(length)]


def get_wrapper_for_type(param_type):
    if param_type == 'int' or param_type == 'long' or param_type == 'short' or param_type == 'byte':
        return arithmetic_arr_value
    elif param_type == 'float' or param_type == 'double':
        return lambda x: get_decimal(param=x)
    elif param_type == 'boolean':
        return lambda x: str(x) == 'True'
    elif param_type == 'char':
        return lambda x: JChar(x.as_string())
    elif param_type == 'String':
        return lambda x: x.as_string()
    return lambda x: x


def arithmetic_arr_value(value):
    return value.as_long()


def get_decimal(param):
    if hasattr(param, 'as_decimal'):
        decimal_str = param.as_decimal(10)
        decimal_str = decimal_str.replace('?', '')
        return float(decimal_str)

    return float(param)
