import re

from definitions import config
from helper.files.fileReader import FileReader


class ParserExampleLoader:
    """
    This class is responsible for loading test examples for the parser
    """

    def __init__(self, file_reader=FileReader):
        self.file_reader = file_reader

    def load_positive_tests(self):
        return self.load(config.POSITIVE_JML_PARSER_FILE)

    def load(self, path: str):
        content = self.file_reader.read(path)
        return self.split(content, '=')

    @staticmethod
    def split(content, symbol):
        """
        Splits the content by the symbol.
        :param content: The content to split.
        :param symbol: The symbol to split by.
        :return: A list of the split content.
        """
        pattern_str = f'^{symbol}{{5,}}$'

        return re.split(pattern_str, content, flags=re.MULTILINE)
