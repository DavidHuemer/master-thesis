from definitions import javaTypes


def get_min_max_values(parameter_type: str):
    """
    Returns the minimum and maximum values for the given parameter type.
    :param parameter_type:
    :return:
    """
    if parameter_type == javaTypes.BYTE_TYPE:
        return -128, 127
    elif parameter_type == javaTypes.SHORT_TYPE:
        return -32768, 32767
    elif parameter_type == javaTypes.INT_TYPE:
        return -(2 ** 31 - 1), 2 ** 31 - 1
    elif parameter_type == javaTypes.LONG_TYPE:
        return -(2 ** 63 - 1), 2 ** 63 - 1
    elif parameter_type == javaTypes.FLOAT_TYPE:
        return -3.4028235e38, 3.4028235e38
    elif parameter_type == javaTypes.DOUBLE_TYPE:
        return -1.7976931348623157e308, 1.7976931348623157e308

    raise Exception(f"Cannot get min and max values for type {parameter_type}")
