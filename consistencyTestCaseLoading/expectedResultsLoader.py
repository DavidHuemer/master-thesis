from definitions import config
from definitions.evaluations.expectedResult import ExpectedResult
from helper.files.fileReader import FileReader


def get_expected_results(file_path=config.EXPECTED_RESULTS_LOCATION):
    expected_file_lines = get_expected_results_file(file_path).split('\n')

    expected_results = [
        parse_expected_result_line(line)
        for line in expected_file_lines
        if line
    ]

    return expected_results


def parse_expected_result_line(expected_result_line):
    expected_result_parts = expected_result_line.split(';')
    if len(expected_result_parts) != 3:
        raise RuntimeError("Expected result line does not have 3 parts")

    java_file_path, method_name, expected_result = expected_result_parts
    return ExpectedResult(java_file_path, method_name, expected_result.lower() == 'true')


def get_expected_results_file(file_path):
    return FileReader.read(file_path)
