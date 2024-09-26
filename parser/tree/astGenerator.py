import io
import sys

from antlr4 import *
from antlr4.error.Errors import InputMismatchException
from antlr4.tree.Tree import ErrorNodeImpl

import parser.generated.JMLLexer as JMLLexer
import parser.generated.JMLParser as JMLParser
from definitions.ast.jmlTreeNode import JmlTreeNode
from definitions.parser.jmlParserResult import JMLParserResult
from definitions.parser.parserException import ParserException
from definitions.parser.parserResult import ParserResult
from helper.logs.loggingHelper import LoggingHelper
from parser.simplifier.jmlSimplifier import JmlSimplifier


class AstGenerator:
    def __init__(self, simplifier=JmlSimplifier()):
        self.simplifier = simplifier

    def get_ast(self, jml: str) -> JmlTreeNode:
        try:
            # First get original parser from ANTLR
            LoggingHelper.log_info("Getting AST from JML")
            parser_result = self.parse(jml)
            LoggingHelper.log_info("JML parsed successfully - Simplifying AST")
            ast = self.simplifier.simplify(parser_result.tree, parser_result.parser_result)
            LoggingHelper.log_info("AST simplified successfully")
            return ast
        except InputMismatchException:
            raise ParserException("Error while parsing initial AST.")

    def parse(self, jml: str) -> JMLParserResult:
        try:
            jml = jml.replace("//", "")
            # Replace surrounding ```java with nothing if it exists
            if jml.startswith("```"):
                # jml is the whole jml without the first and last line
                # So we need to remove the first and last line
                jml = jml.split("\n")[1:-1]
                jml = "\n".join(jml)

            sys.stderr = io.StringIO()

            lexer = JMLLexer.JMLLexer(InputStream(jml))
            stream = CommonTokenStream(lexer)
            jml_parser = JMLParser.JMLParser(stream)

            tree = jml_parser.jml()

            if tree.exception is not None:
                raise tree.exception

            # If the tree contains a ErrorNodeImpl then raise an exception
            error_node = self.has_error_node_implementation(tree)

            if error_node is not None:
                raise ParserException("Error while parsing initial AST.",
                                      error_node=error_node)

            return JMLParserResult(ParserResult(lexer, jml_parser), tree)
        except InputMismatchException:
            raise ParserException("Error while parsing initial AST.")
        finally:
            sys.stderr = sys.__stderr__

    def has_error_node_implementation(self, tree):
        if hasattr(tree, 'children') and tree.children is not None:
            for child in tree.children:
                error_node = self.has_error_node_implementation(child)
                if error_node is not None:
                    return error_node

        if isinstance(tree, ErrorNodeImpl):
            return str(tree)

        return None
