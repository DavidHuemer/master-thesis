from parser.tree.parserErrorListener import ParserErrorListener


class ParserErrorContainer:
    def __init__(self):
        self.lexer_error_listener = ParserErrorListener()
        self.parser_error_listener = ParserErrorListener()

    def has_errors(self):
        return len(self.lexer_error_listener.errors) > 0 or len(self.parser_error_listener.errors) > 0

    def get_errors(self):
        return self.lexer_error_listener.errors + self.parser_error_listener.errors
