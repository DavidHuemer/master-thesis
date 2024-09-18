import importlib

from definitions import config
from helper.logs.loggingHelper import LoggingHelper
from parser.generated import JMLLexer, JMLParser
from parser.parserEnvironmentChecker import ParserEnvironmentChecker
from parser.test.parserTestRunner import ParserTestRunner
from parser.update.parserUpdater import ParserUpdater


class ParserUpdatePipeline:
    """
    Pipeline that updates and tests the ANTLR parser
    """

    def __init__(self, parser_environment_checker=ParserEnvironmentChecker(), parser_updater=ParserUpdater()):
        """
        Initialize the pipeline
        :param parser_environment_checker: Is used for checking the environment (Whether the parser is set up correctly)
        :param parser_updater: Is used for updating the parser
        """
        self.parser_environment_checker = parser_environment_checker
        self.parser_updater = parser_updater

    def run_update_pipeline(self, parser_file_path=config.PARSER_FILE):
        """
        Run the update pipeline
        """

        # First check environment
        if not self.parser_environment_checker.check_environment(parser_file_path):
            LoggingHelper.log_error("The environment is not set up correctly for the parser")
            return

        # Then build the parser
        self.parser_updater.update(parser_file_path)

        self.reload_modules()

        # Then test the parser
        self.run_tests()

    @staticmethod
    def reload_modules():
        """
        Reloads teh antlr generated modules
        """
        importlib.reload(JMLLexer)
        importlib.reload(JMLParser)

    @staticmethod
    def run_tests():
        """
        Run the parser tests (To check if the parser is working correctly)
        """
        ParserUpdatePipeline.get_test_runner().run_tests()

    @staticmethod
    def get_test_runner():
        """
        Get the test runner
        :return: The test runner
        """
        return ParserTestRunner()
