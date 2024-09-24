import os

from definitions.consistencyTestCase import ConsistencyTestCase
from definitions.evaluations.expectedResult import ExpectedResult
from definitions.javaCode import JavaCode
from definitions.javaMethod import JavaMethod
from testCases.expectedResultFinder import ExpectedResultFinder


class ConsistencyTestCaseBuilder:
    """
    A class that builds consistency test cases.
    """

    def __init__(self, expected_result_finder=ExpectedResultFinder):
        self.expected_result_finder = expected_result_finder

    def build_test_cases(self, expected_results: list[ExpectedResult], java_code_list: list[JavaCode]) \
            -> list[ConsistencyTestCase]:
        """
        Returns the consistency test cases based on the given expected results and java code list.
        :param expected_results: The expected results
        :param java_code_list: The actual java code list containing the methods to be tested
        :return: The consistency test cases
        """

        return [self.build_test_case(java_code, method, expected_results)
                for java_code in java_code_list
                for method in java_code.methods]

    def build_test_case(self, java_code: JavaCode, method: JavaMethod, expected_results: list[ExpectedResult]) \
            -> ConsistencyTestCase:
        """
        Builds a consistency test case based on the given java code, method, and expected results.
        :param java_code: The java code containing the method to run
        :param method: The actual method that will be tested
        :param expected_results: All the expected results
        :return: The consistency test case
        """

        # Check if there are expected results for the java file
        expected_result = self.expected_result_finder.get_expected_result_for_code(java_code, method, expected_results)

        return ConsistencyTestCase(java_code, method, expected_result)
