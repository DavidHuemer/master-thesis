from prettytable import PrettyTable

from definitions.verification.verificationResult import VerificationResult
from helper.logs.loggingHelper import log_info


def write_test_cases_table(test_results: list[VerificationResult]):
    """
    Write a table with the test cases and their results
    """

    table = PrettyTable()
    table.field_names = ['Test case name', 'Expected result', 'Result']

    invalid_test_results = [test_result for test_result in test_results if
                            test_result.get_expected_result() is None
                            or test_result.get_expected_result() != test_result.consistent]

    for test_result in invalid_test_results:
        name = get_name(test_result)
        expected_result = get_expected_result_str(test_result)
        result = get_result_str(test_result)
        table.add_row([name, expected_result, result])

    table_str = table.get_string()
    log_info("Incorrect test cases:")
    log_info(table_str)


def get_name(test_result: VerificationResult) -> str:
    return test_result.consistency_test_case.get_name()


def get_expected_result_str(test_result: VerificationResult) -> str:
    if test_result.get_expected_result() is not None:
        if test_result.get_expected_result():
            return "Consistent"
        else:
            return "Not consistent"

    return "?"


def get_result_str(test_result: VerificationResult) -> str:
    if test_result.consistent is True:
        return "Consistent"
    elif test_result.consistent is False:
        return "Not consistent"
    else:
        return "?"
