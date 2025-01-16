from definitions.evaluations.expectedResult import ExpectedResult
from definitions.javaCode import JavaCode
from definitions.javaMethod import JavaMethod


class ConsistencyTestCase:
    """
    A test case that represents a check for inconsistencies in the code documentation.
    """

    def __init__(self, java_code: JavaCode, method_info: JavaMethod, expected_result: ExpectedResult | None):
        """
        Constructor for the ConsistencyTestCase class.
        :param java_code: The java code
        :param method_info: The method information
        :param expected_result: The expected result
        """
        self.java_code = java_code
        self.method_info = method_info
        self.expected_result = expected_result

    def get_comment(self):
        """
        Returns the comment of the method.
        :return: The comment of the method
        """
        return self.method_info.comment

    def __eq__(self, other):
        return (self.java_code == other.java_code
                and self.method_info == other.method_info
                and self.expected_result == other.expected_result)

    def __str__(self):
        return (f'{self.get_name()} - '
                f'{self.get_expected_result_str()}')

    def get_name(self):
        return f'{self.java_code.class_name}.{self.method_info.name}'

    def get_expected_result_str(self):
        return self.expected_result.expected_result if self.expected_result is not None else 'No expected result'
