import re

from definitions import config
from definitions.ai.jmlTransormationExample import JmlTransformationExample
from helper.files.fileReader import FileReader


class JmlExamplesLoader:
    """
    This class is responsible for loading the examples from the JML examples file.
    """

    def __init__(self, file_reader=FileReader):
        self.file_reader = file_reader

    def load(self, path=config.JML_TRANSFORMATIONS_EXAMPLES_FILE_PATH) -> list[JmlTransformationExample]:
        """
        Loads the examples from the JML examples file.
        :param path: The path to the JML examples file.
        :return: A list of JML transformation examples.
        """
        examples_content = self.file_reader.read(path)

        example_transformations = self.split(examples_content, '=')

        examples = []

        for example_transformation in example_transformations:
            example_parts = self.split(example_transformation, '-')
            if len(example_parts) != 2:
                continue

            examples.append(JmlTransformationExample(example_parts[0].strip(), example_parts[1].strip()))

        return examples

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
