import os.path

from helper.files.fileHelper import FileHelper
from helper.logs.loggingHelper import LoggingHelper


class FileFinder:
    """
    This class is responsible for finding all files with a specific file extension in a directory.
    """

    def __init__(self, file_helper=FileHelper):
        """
        Initializes a new instance of the FileFinder class.
        :param file_helper: The file helper to use.
        """
        self.file_helper = file_helper

    def find(self, directory_path, file_extension):
        """
        Finds all files with the given file extension in the given directory.

        It searches recursively in all subdirectories.
        :param directory_path: The directory to search in.
        :param file_extension: The file extension to search for.
        :return: A list of all files with the given file extension in the given directory.
        """
        files = []

        try:
            # Include files from subdirectories
            for sub_directory_path in self.file_helper.get_directories_by_path(directory_path):
                files += self.find(sub_directory_path, file_extension)

            # Include files from the current directory
            for file in self.file_helper.get_files_by_path(directory_path,
                                                           lambda f: self.check_file_extension(f, file_extension)):
                files.append(file)

        except FileNotFoundError:
            LoggingHelper.log_warning(f"Directory '{directory_path}' not found. Could not search for files.")

        return files

    @staticmethod
    def check_file_extension(file, file_extension):
        """
        Checks if the given file has the correct file extension.
        :param file: The file to check.
        :param file_extension: The file extension to check for.
        :return: Whether the file has the correct file extension.
        """
        parts = os.path.splitext(file)
        return len(parts) == 2 and parts[1] == f'.{file_extension}'
