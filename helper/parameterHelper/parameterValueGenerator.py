import jpype

from definitions.parameters.parameterValue import ParameterValue

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
    jpype.JString: str,
    jpype.JArray: list
}


def python_to_java(python_value, java_type: str):
    if python_value is None:
        return None

    if isinstance(python_value, list):
        return jpype.JArray(java_types_map[java_type.lower()], 1)(python_value)

    for key in java_types_map:
        if java_type.lower() == key.lower():
            return java_types_map[key](python_value)


def get_parameter_value_by_python(python_value, java_type: str) -> ParameterValue:
    return ParameterValue(python_value, python_to_java(python_value, java_type))


def java_to_python(java_value):
    if java_value is None:
        return None

    for java_type in java_to_python_map:
        if isinstance(java_value, java_type):
            return java_to_python_map[java_type](java_value)

        if isinstance(java_value, java_to_python_map[java_type]):
            return java_value

    raise ValueError(f"Unsupported type to convert into python type: {java_value}")


def get_parameter_value_by_java(java_value) -> ParameterValue:
    return ParameterValue(java_to_python(java_value), java_value)
