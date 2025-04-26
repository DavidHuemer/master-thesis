import jpype
from jpype import JString

from definitions.code.parameterExtractionInfo import ParameterExtractionInfo
from definitions.evaluations.csp.parameters.methodCallParameter import MethodCallParameter
from definitions.evaluations.csp.parameters.methodCallParameters import MethodCallParameters
from definitions.verification.testCase import TestCase

java_types_map = {
    "int": jpype.JInt,
    "float": jpype.JFloat,
    "double": jpype.JDouble,
    "long": jpype.JLong,
    "short": jpype.JShort,
    "byte": jpype.JByte,
    "char": jpype.JChar,
    "boolean": jpype.JBoolean,
    "string": jpype.JString
}

java_to_python_map = {
    jpype.JInt: int,
    jpype.JFloat: float,
    jpype.JDouble: float,
    jpype.JLong: int,
    jpype.JShort: int,
    jpype.JByte: int,
    jpype.JChar: str,
    jpype.JBoolean: bool,
    JString: str,
    jpype.JArray: list
}

java_type_to_python_map = {
    "java.lang.Integer": int,
    "java.lang.Double": float,
    "java.lang.Float": float,
    "java.lang.Long": int,
    "java.lang.Short": int,
    "java.lang.Byte": int,
    "java.lang.Boolean": bool,
    "java.lang.Character": str,
    "java.lang.String": str,
    "java.lang.Array": list
}


# def to_java_type(value) -> jpype.JObject:
#     if isinstance(value, list):
#         return jpype.JArray(jpype.JInt, 1)(value)
#
#     for key in java_types_map:
#         if isinstance(value, key):
#             return java_types_map[key](value)

def get_java_parameter(value, parameter_info: ParameterExtractionInfo):
    if isinstance(value, list):
        return jpype.JArray(jpype.JInt, 1)(value)

    for key in java_types_map:
        if parameter_info.variable_type.lower() == key.lower():
            return java_types_map[key](value)

    raise ValueError(f"Unsupported type to convert into java type: {parameter_info.variable_type}")


def get_java_parameters(test_case: TestCase, parameter_infos: list[ParameterExtractionInfo]) -> MethodCallParameters:
    method_call_parameters = MethodCallParameters()

    for parameter_info in parameter_infos:
        param_value = test_case.parameters[parameter_info.name]
        java_param_value = get_java_parameter(param_value, parameter_info) if param_value is not None else None
        method_call_parameters[parameter_info.name] = MethodCallParameter(java_param_value)

    return method_call_parameters


def get_python_from_java(java_object):
    for java_type in java_to_python_map:
        if isinstance(java_object, java_type):
            return java_to_python_map[java_type](java_object)

        if isinstance(java_object, java_to_python_map[java_type]):
            return java_object

    raise ValueError(f"Unsupported type to convert into python type: {java_object}")


def get_python_value_from_original_java(java_object):
    """
    Returns the python value from the original java object (java.lang.<type>).
    For example, java.lang.Double will be converted to float.
    :param java_object: The java object to convert.
    :return: The python value.
    """
    java_type_str = java_object.getClass().getName()
    if java_type_str in java_type_to_python_map:
        return java_type_to_python_map[java_type_str](java_object)

    raise ValueError(f"Unsupported type to convert into python type: {java_object}")


def get_type_as_string_from_java_value(java_value):
    """
    Returns the type of the java value as a string.
    For example JDouble will be returned as "double".
    :param java_value: The java value to get the type from.
    :return: The type of the java value as a string.
    """
    pass
