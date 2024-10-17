from antlr4.error.ErrorListener import ErrorListener

from definitions.parser.parserError import ParserError


class ParserErrorListener(ErrorListener):
    def __init__(self):
        super(ParserErrorListener, self).__init__()
        self.errors: list[ParserError] = []

    def syntaxError(self, recognizer, offendingSymbol, line, column, msg, e):
        self.errors.append(ParserError(line, column, msg))
