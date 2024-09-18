from definitions import config
from helper.files.fileHelper import FileHelper
from helper.logs.loggingHelper import LoggingHelper
from helper.processHelper import ProcessHelper


class ParserEnvironmentChecker:
    """
    Class that is used to check if the environment is set up correctly for the parser.
    """

    def __init__(self, process_helper=ProcessHelper, file_helper=FileHelper):
        self.process_helper = process_helper
        self.file_helper = file_helper

    def check_environment(self, parser_file: str) -> bool:
        """
        Check if the environment is set up correctly for the parser
        :return: True if the environment is set up correctly, False otherwise
        """

        if not self.check_java():
            LoggingHelper.log_error("Java is not installed")
            return False

        LoggingHelper.log_info("Java is installed")

        if not self.check_antlr_tool():
            LoggingHelper.log_error("The antlr tool is not installed")
            return False

        LoggingHelper.log_info("The antlr tool is installed")

        if not self.check_parser_file(parser_file):
            LoggingHelper.log_error("The parser file is not found")
            return False

        LoggingHelper.log_info("The parser file is found")

        return True

    def check_java(self):
        """
        Check if java is installed
        :return: True if java is installed, False otherwise
        """

        return self.process_helper.check_with_commands(["java", "--version"])

    def check_antlr_tool(self):
        """
        Check if the antlr tool is installed
        :return: True if the antlr tool is installed, False otherwise
        """
        return self.process_helper.check_with_commands(
            ["java", "-cp", config.ANTLR_JAR_PATH, config.ANTLR_COMMAND])

    def check_parser_file(self, parser_file: str):
        return self.file_helper.exists(parser_file)
