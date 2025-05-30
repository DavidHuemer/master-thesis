import io
import sys

import parser.generated.JMLLexer as JMLLexer
import parser.generated.JMLParser as JMLParser
from antlr4.CommonTokenStream import CommonTokenStream
from antlr4.InputStream import InputStream
from antlr4.error.Errors import InputMismatchException

from definitions.parser.jmlParserResult import JMLParserResult
from definitions.parser.parserException import ParserException
from definitions.parser.parserResult import ParserResult
from helper.logs.loggingHelper import log_info
from parser.simplifier.jmlSimplifier import JmlSimplifier
from parser.tree.jmlBeautifier import beautify_jml
from parser.tree.parserErrorContainer import ParserErrorContainer


def get_ast_by_jml(jml: str):
    log_info("Getting AST from JML")
    parser_result = parse_jml(jml)
    jml_simplifier = JmlSimplifier()
    log_info("JML parsed successfully - Simplifying AST")
    ast = jml_simplifier.simplify(parser_result.tree, parser_result.parser_result)
    log_info("AST simplified successfully")
    return ast


def parse_jml(jml: str) -> JMLParserResult:
    jml = beautify_jml(jml)
    sys.stderr = io.StringIO()
    parser_error_container = ParserErrorContainer()

    try:
        jml_lexer = get_lexer(jml, parser_error_container)
        jml_parser = get_parser(jml_lexer, parser_error_container)
        tree = jml_parser.jml()

        if parser_error_container.has_errors():
            raise ParserException(parser_error_container.get_errors())

        return JMLParserResult(ParserResult(jml_lexer, jml_parser), tree)
    except InputMismatchException:
        raise Exception("Error while parsing initial AST")
    finally:
        sys.stderr = sys.__stderr__


def get_lexer(jml: str, error_container: ParserErrorContainer):
    lexer = JMLLexer.JMLLexer(InputStream(jml))
    lexer.removeErrorListeners()
    lexer.addErrorListener(error_container.lexer_error_listener)
    return lexer


def get_parser(lexer, error_container: ParserErrorContainer):
    stream = CommonTokenStream(lexer)
    jml_parser = JMLParser.JMLParser(stream)
    jml_parser.removeErrorListeners()
    jml_parser.addErrorListener(error_container.parser_error_listener)
    return jml_parser
