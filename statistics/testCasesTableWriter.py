from prettytable import PrettyTable

from definitions.verification.verificationResult import VerificationResult
from helper.logs.loggingHelper import LoggingHelper


class TestCasesTableWriter:
    def write_test_cases_table(self, test_results: list[VerificationResult]):
        """
        Write a table with the test cases and their results
        """

        table = PrettyTable()
        table.field_names = ['Test case name', 'Expected result', 'Result']

        for test_result in test_results:
            name = self.get_name(test_result)
            expected_result = self.get_expected_result_str(test_result)
            result = self.get_result_str(test_result)
            table.add_row([name, expected_result, result])

        table_str = table.get_string()
        LoggingHelper.log_info("Test cases table:")
        LoggingHelper.log_info(table_str, show_level=False)

    @staticmethod
    def get_name(test_result: VerificationResult) -> str:
        return test_result.consistency_test_case.get_name()

    @staticmethod
    def get_expected_result_str(test_result: VerificationResult) -> str:
        if test_result.consistency_test_case.expected_result is not None:
            if test_result.consistency_test_case.expected_result.expected_result:
                return "Consistent"
            else:
                return "Not consistent"

        return "?"

    @staticmethod
    def get_result_str(test_result: VerificationResult) -> str:
        if test_result.consistent is True:
            return "Consistent"
        elif test_result.consistent is False:
            return "Not consistent"
        else:
            return "?"
