from definitions.parser.parserError import ParserError


class ParserException(Exception):
    def __init__(self, parser_errors: list[ParserError]):
        super().__init__("Parser exception occurred")
        self.parser_errors = parser_errors
