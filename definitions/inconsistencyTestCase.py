from definitions.evaluations.expectedResult import ExpectedResult
from definitions.javaCode import JavaCode
from definitions.javaMethod import JavaMethod


class InconsistencyTestCase:
    """
    A test case that checks for inconsistencies in the code documentation.
    """

    def __init__(self, java_code: JavaCode, method_info: JavaMethod, expected_result: ExpectedResult | None):
        """
        Constructor for the InconsistencyTestCase class.
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
