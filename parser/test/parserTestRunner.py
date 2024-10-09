from helper.logs.loggingHelper import LoggingHelper
from parser.test.parserExampleLoader import ParserExampleLoader
from parser.tree.astGenerator import AstGenerator


class ParserTestRunner:
    """
    This class is used to run the parser tests.
    """

    def __init__(self, parser_test_example_loader=ParserExampleLoader(), ast_generator=AstGenerator()):
        self.parser_test_example_loader = parser_test_example_loader
        self.ast_generator = ast_generator

    def run_tests(self):
        """
        Run the parser tests
        """
        self.run_positive_tests()
        self.run_negative_tests()

    def run_positive_tests(self):
        """
        Run the tests that should be able to be parsed
        """

        LoggingHelper.log_info("Running positive tests")
        examples = self.parser_test_example_loader.load_positive_tests()

        for example in examples:
            try:
                ast = self.ast_generator.get_ast(example)
                LoggingHelper.log_info(ast.get_tree_string())
                LoggingHelper.log_info(f"Example parsed successfully")
            except Exception as e:
                LoggingHelper.log_error(f"Error parsing example:\n {example}")
                LoggingHelper.log_error(e)

    @staticmethod
    def run_negative_tests():
        """
        Run the tests that should not be able to be parsed
        """

        LoggingHelper.log_info("Running negative tests")
