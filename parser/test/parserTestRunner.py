from helper.logs.loggingHelper import log_info, log_error
from parser.test.parserExampleLoader import ParserExampleLoader
from parser.tree.astGenerator import get_ast_by_jml


class ParserTestRunner:
    """
    This class is used to run the parser tests.
    """

    def __init__(self, parser_test_example_loader=ParserExampleLoader()):
        self.parser_test_example_loader = parser_test_example_loader

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

        log_info("Running positive tests")
        examples = self.parser_test_example_loader.load_positive_tests()

        for example in examples:
            try:
                ast = get_ast_by_jml(example)
                log_info(ast.get_tree_string())
                log_info(f"Example parsed successfully")
            except Exception as e:
                log_error(f"Error parsing example:\n {example}")
                log_error(e)

    @staticmethod
    def run_negative_tests():
        """
        Run the tests that should not be able to be parsed
        """

        log_info("Running negative tests")
