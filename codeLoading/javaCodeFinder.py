from helper.files.fileFinder import FileFinder


class JavaCodeFinder:
    """
    This class is used to find Java code
    :param file_finder: The file finder object used to find files.
    """

    def __init__(self, file_finder=FileFinder()):
        self.code_finder = file_finder
        pass

    def get_java_file_paths_from_directory(self, directory_path):
        """
        Returns all Java file paths from the given directory path.
        It also returns all Java file paths from all subdirectories.
        :param directory_path: The directory path.
        :return: List of Java file paths.
        """

        return self.code_finder.find(directory_path, "java")
