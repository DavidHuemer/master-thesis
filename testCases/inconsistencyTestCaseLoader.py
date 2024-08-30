from codeLoading.javaCodeLoader import JavaCodeLoader
from definitions import config
from evaluation.expectedResultsLoader import ExpectedResultsLoader
from testCases.inconsistencyTestCaseBuilder import InconsistencyTestCaseBuilder


class InconsistencyTestCaseLoader:
    """
    This class is responsible for loading the test cases, that are checked for inconsistencies.
    """

    def __init__(self, expected_results_loader=ExpectedResultsLoader(), java_code_loader=JavaCodeLoader(),
                 builder=InconsistencyTestCaseBuilder()):
        """
        Initializes the TestCaseLoader object.
        :param expected_results_loader: The loader for the expected results
        :param java_code_loader: The loader for the java code
        """
        self.expected_results_loader = expected_results_loader
        self.java_code_loader = java_code_loader
        self.builder = builder

    def get_test_cases(self, code_directory_path=config.CODE_DIRECTORY):
        """
        Returns the existing test cases for the given code directory.
        :param code_directory_path: The path to the code directory
        :return: The test cases
        """
        expected_results = self.expected_results_loader.get_expected_results()
        java_code_list = self.java_code_loader.get_java_code_from_directory(code_directory_path)

        return self.builder.build_test_cases(expected_results, java_code_list)
