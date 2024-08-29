from codeLoading.codeReader.javaCodeReader import JavaCodeReader
from codeLoading.javaCodeFinder import JavaCodeFinder
from definitions.javaCode import JavaCode
from helper.logs.loggingHelper import LoggingHelper


class JavaCodeLoader:
    def __init__(self, java_code_finder=JavaCodeFinder(), java_code_reader=JavaCodeReader()):
        """
        Initializes the JavaCodeLoader object.
        :param java_code_finder: The Java code finder that is used to find Java code.
        :param java_code_reader: The Java code reader that is used to read Java code.
        """
        self.code_finder = java_code_finder
        self.java_code_reader = java_code_reader

    def get_java_code_from_directory(self, directory_path) -> list[JavaCode]:
        """
        Returns all Java code from the given directory path.
        It also returns all Java code from all subdirectories.
        :param directory_path: The directory path.
        :return: List of Java code.
        """

        java_files = self.code_finder.get_java_file_paths_from_directory(directory_path)
        LoggingHelper.log_info(f'Found {len(java_files)} Java file(s) in directory "{directory_path}"')

        return self.get_java_code_from_files(java_files)

    def get_java_code_from_files(self, file_paths) -> list[JavaCode]:
        """
        Returns all Java code from the given file paths.
        :param file_paths: The file paths to the Java files.
        :return: List of Java code.
        """

        java_code = []

        for file_path in file_paths:
            try:
                java_code.append(self.java_code_reader.get_java_from_file(file_path))
            except Exception as e:
                LoggingHelper.log_error(f'Error while reading Java code from file "{file_path}": {e}')

        return java_code
