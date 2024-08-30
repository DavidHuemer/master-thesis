from definitions.evaluations.expectedResult import ExpectedResult


def get_expected_result_example(file_path="file_path", method_name="method_name",
                                expected_result="true") -> ExpectedResult:
    return ExpectedResult(file_path, method_name, expected_result)
