import io
import sys

import parser.generated.JMLLexer as JMLLexer
import parser.generated.JMLParser as JMLParser
from antlr4 import *
from antlr4.error.Errors import InputMismatchException

from definitions.ast.jmlTreeNode import JmlTreeNode
from definitions.parser.jmlParserResult import JMLParserResult
from definitions.parser.parserException import ParserException
from definitions.parser.parserResult import ParserResult
from helper.logs.loggingHelper import LoggingHelper
from parser.simplifier.jmlSimplifier import JmlSimplifier
from parser.tree.jmlBeautifier import JMLBeautifier
from parser.tree.parserErrorContainer import ParserErrorContainer


class AstGenerator:
    def __init__(self, simplifier=JmlSimplifier(), jml_beautifier=JMLBeautifier()):
        self.simplifier = simplifier
        self.jml_beautifier = jml_beautifier

    def get_ast(self, jml: str) -> JmlTreeNode:
        # First get original parser from ANTLR
        LoggingHelper.log_info("Getting AST from JML")
        parser_result = self.parse(jml)
        LoggingHelper.log_info("JML parsed successfully - Simplifying AST")
        ast = self.simplifier.simplify(parser_result.tree, parser_result.parser_result)
        LoggingHelper.log_info("AST simplified successfully")
        return ast

    def parse(self, jml: str) -> JMLParserResult:
        try:
            jml = self.jml_beautifier.beautify(jml)

            sys.stderr = io.StringIO()
            parser_error_container = ParserErrorContainer()

            jml_lexer = self.get_lexer(jml, parser_error_container)
            jml_parser = self.get_parser(jml_lexer, parser_error_container)
            tree = jml_parser.jml()

            if parser_error_container.has_errors():
                raise ParserException(parser_error_container.get_errors())

            return JMLParserResult(ParserResult(jml_lexer, jml_parser), tree)
        except InputMismatchException:
            raise Exception("Error while parsing initial AST")
        finally:
            sys.stderr = sys.__stderr__

    @staticmethod
    def get_lexer(jml: str, error_container: ParserErrorContainer):
        lexer = JMLLexer.JMLLexer(InputStream(jml))
        lexer.removeErrorListeners()
        lexer.addErrorListener(error_container.lexer_error_listener)
        return lexer

    @staticmethod
    def get_parser(lexer, error_container: ParserErrorContainer):
        stream = CommonTokenStream(lexer)
        jml_parser = JMLParser.JMLParser(stream)
        jml_parser.removeErrorListeners()
        jml_parser.addErrorListener(error_container.parser_error_listener)
        return jml_parser
