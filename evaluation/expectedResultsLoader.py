from definitions import config
from definitions.evaluations.expectedResult import ExpectedResult
from helper.files.fileReader import FileReader
from helper.logs.loggingHelper import LoggingHelper


class ExpectedResultsLoader:
    """
    Class to load the expected results
    """

    def __init__(self, file_reader=FileReader):
        self.file_reader = file_reader

    def get_expected_results(self, file_path=config.EXPECTED_RESULTS_LOCATION) -> list[ExpectedResult]:
        """
        Returns the expected results from the given file path
        :param file_path: The file path to the expected results file
        :return: The expected results
        """

        expected_file_content = self.get_expected_results_file(file_path)
        expected_file_lines = expected_file_content.split('\n')

        expected_results = []

        for expected_file_line in expected_file_lines:
            try:
                expected_results.append(self.parse_expected_result_line(expected_file_line))
            except RuntimeError:
                LoggingHelper.log_warning(f'Could not parse expected result line: {expected_file_line}')

        return expected_results

    def get_expected_results_file(self, file_path=config.EXPECTED_RESULTS_LOCATION) -> str:
        """
        Returns the expected results file
        :param file_path: The file path to the expected results file
        :return: The expected results file
        """

        return self.file_reader.read(file_path)

    @staticmethod
    def parse_expected_result_line(expected_result_line) -> ExpectedResult:
        """
        Parses the expected result line
        :param expected_result_line: The expected result line
        :return: The parsed expected result line
        """

        expected_result_parts = expected_result_line.split(';')
        if len(expected_result_parts) != 3:
            raise RuntimeError("Expected result line does not have 3 parts")

        java_file_path, method_name, expected_result = expected_result_parts
        return ExpectedResult(java_file_path, method_name, expected_result.lower() == 'true')
