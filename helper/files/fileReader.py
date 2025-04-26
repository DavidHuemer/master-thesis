def read_file(file_path):
    with open(file_path, 'r') as file:
        return file.read()


class FileReader:
    """
    Class to read a file
    """

    @staticmethod
    def read(path):
        """
        Read the content of a file with the given path
        :param path: The path of the file
        :return: The content of the file
        """
        with open(path, 'r') as file:
            return file.read()
