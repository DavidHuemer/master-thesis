import os

from definitions.evaluations.expectedResult import ExpectedResult
from definitions.javaCode import JavaCode
from definitions.javaMethod import JavaMethod


class ExpectedResultFinder:
    """
    Class for finding the expected result for a given java file and method.
    """

    @staticmethod
    def get_expected_result_for_code(java_code: JavaCode, method: JavaMethod,
                                     expected_results: list[ExpectedResult]) -> ExpectedResult | None:
        """
        Returns the expected result for the given java file and method.
        :param java_code: The java code containing the file path
        :param method: The method to be tested
        :param expected_results: The list of expected results to search through
        :return: The expected result if found, otherwise None
        """

        # Check if there are expected results for the java file
        expected_results_for_file = list(
            filter(lambda result: os.path.normpath(result.file_path) == os.path.normpath(
                java_code.file_path) and result.method_name == method.name,
                   expected_results))

        return expected_results_for_file[0] if len(expected_results_for_file) > 0 else None
