import os

from codetiming import Timer

from consistencyTestCaseLoading.javaCodeLoading import get_java_code_from_directory
from definitions.consistencyTestCase import ConsistencyTestCase
from definitions.evaluations.expectedResult import ExpectedResult
from definitions.javaCode import JavaCode
from definitions.javaMethod import JavaMethod
from consistencyTestCaseLoading.expectedResultsLoader import get_expected_results
from helper.logs.loggingHelper import log_info

get_test_cases_timer = Timer(name="get_test_cases", logger=None)


@get_test_cases_timer
def get_test_cases() -> list[ConsistencyTestCase]:
    log_info("Loading consistency test cases")

    # First get expected results
    expected_results = get_expected_results()

    # Get java code list
    java_code = get_java_code_from_directory()

    # Build test cases
    return build_test_cases(expected_results, java_code)


def build_test_cases(expected_results, java_code) -> list[ConsistencyTestCase]:
    return [build_test_case(java_code, method, expected_results)
            for java_code in java_code
            for method in java_code.methods
            if method.comment is not None and method.method_protection == 'public']


def build_test_case(java_code, method, expected_results: list[ExpectedResult]) -> ConsistencyTestCase:
    expected_result = get_expected_result_for_code(java_code, method, expected_results)
    return ConsistencyTestCase(java_code, method, expected_result)


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
    return next(
        (result for result in expected_results
         if os.path.normpath(result.file_path) == os.path.normpath(
            java_code.file_path) and result.method_name == method.name),
        None
    )
