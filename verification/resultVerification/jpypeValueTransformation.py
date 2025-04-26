from jpype import JBoolean, JDouble, JInt, JString, JChar


def transform_to_jpype_value(value):
    if isinstance(value, JChar):
        return value
    if isinstance(value, str):
        return JString(value)
    elif isinstance(value, int):
        return JInt(value)
    elif isinstance(value, float):
        return JDouble(value)
    elif isinstance(value, bool):
        return JBoolean(value)

    return value
