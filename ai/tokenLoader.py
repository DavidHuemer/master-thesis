from definitions import config
from helper.files.fileReader import FileReader


class TokenLoader:
    """
    This class is responsible for loading the API key from a file.
    """

    def __init__(self, file_reader=FileReader):
        """
        Initialize the token loader.
        :param file_reader: The file reader that is used to read the API key from a file.
        """
        self.file_reader = file_reader

    def load(self, path: str = config.API_KEY_PATH) -> str:
        """
        Load the API key from the file.
        :param path: The path to the file that contains the API key.
        :return: The API key.
        """
        return self.file_reader.read(path)
