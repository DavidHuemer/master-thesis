from antlr4 import *
from antlr4 import CommonTokenStream
from antlr4.error.Errors import InputMismatchException

import parser.generated.JMLLexer as JMLLexer
import parser.generated.JMLParser as JMLParser
from definitions.ast.jmlTreeNode import JmlTreeNode
from definitions.parser.parserException import ParserException
from definitions.parser.parserResult import ParserResult
from parser.simplifier.jmlSimplifier import JmlSimplifier


class AstGenerator:
    def __init__(self, simplifier=JmlSimplifier()):
        self.simplifier = simplifier

    def get_ast(self, jml: str) -> JmlTreeNode:
        try:
            # First get original parser from ANTLR
            parser_result = self.parse(jml)

            tree = parser_result.jml_parser.jml()

            if tree.exception is not None:
                raise tree.exception

            ast = self.simplifier.simplify(tree, parser_result)
            return ast
        except InputMismatchException as e:
            raise ParserException("Error while parsing initial AST.")

    @staticmethod
    def parse(jml: str) -> ParserResult:
        # Remove // from input jml
        jml = jml.replace("//", "")

        lexer = JMLLexer.JMLLexer(InputStream(jml))
        stream = CommonTokenStream(lexer)
        jml_parser = JMLParser.JMLParser(stream)

        return ParserResult(lexer, jml_parser)
