from definitions import config
from definitions.evaluations.expectedResult import ExpectedResult
from helper.files.jsonFileHelper import JsonFileHelper


def get_expected_results(file_path=config.EXPECTED_RESULTS_LOCATION):
    expected_json = JsonFileHelper.read_json_file(file_path)
    return [ExpectedResult(file_path=expected_result['path'],
                           method_name=expected_result['method'],
                           expected_result=expected_result['expectedResult'],
                           category=expected_result['category'])
            for expected_result in expected_json]
