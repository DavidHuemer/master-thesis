from definitions.parser.parserError import ParserError


class ParserException(Exception):
    def __init__(self, parser_errors: list[ParserError]):
        parser_str = "Parser exception occurred"
        if len(parser_errors) > 0:
            parser_str += f":\n{'\n'.join([str(x) for x in parser_errors])}"
        super().__init__(parser_str)
