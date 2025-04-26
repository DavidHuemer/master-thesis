from definitions.consistencyTestCase import ConsistencyTestCase
from definitions.parameters.parameter import Parameter
from helper.parameterHelper.parameterGenerator import get_initial_parameter
from helper.parameterHelper.parameterValueGenerator import get_parameter_value_by_python
from testGeneration.testCaseGeneration.javaTypeMapper import get_python_value_converter
from verification.csp.cspParamBuilder import build_csp_param


class ReturnTypeConverter:
    """
    Responsible for converting the return value of a java method into a parameter
    """

    @staticmethod
    def get_return_parameter(result_java, test_case: ConsistencyTestCase):
        """
        Returns the return value as a parameter
        :param result_java: The java value that was returned from the java method
        :param test_case: The test case that was executed
        :return: The return value as a parameter
        """
        if (test_case.method_info.return_type is None
                or test_case.method_info.return_type.variable_type.lower() == "void"):
            return None

        java_type = test_case.method_info.return_type.variable_type
        dimension = test_case.method_info.return_type.dimension

        result_param = get_initial_parameter(java_type, "\\result", dimension)

        converter = get_python_value_converter(java_type)

        # Initialize the result_parameter with the actual value
        if result_java is None:
            python_value = None
        elif dimension > 0:
            python_value = [converter(java_element) for java_element in result_java]
        else:
            python_value = converter(result_java)

        parameter_value = get_parameter_value_by_python(python_value, java_type)
        result_param.old.parameter_value = parameter_value
        return result_param

    @staticmethod
    def get_return_csp_param(java_type: str, dimension: int):
        csp_parameter = build_csp_param(java_type, "\\result", dimension=dimension)


def get_return_parameter(result_java, test_case: ConsistencyTestCase) -> Parameter | None:
    pass
    # if result_java is None:
