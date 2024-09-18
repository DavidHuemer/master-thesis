import os
import shutil


class FileHelper:
    """
    A helper class for file operations.
    """

    @staticmethod
    def get_directories_by_path(path, pred=lambda f: True):
        """
        Returns all directories of a given path.
        :param path: The path in which the directories are searched.
        :param pred: The predicate to filter the directories.
        :return: A list of all directories in the given path.
        """
        return FileHelper.get_entries_by_path(path, lambda f: f.is_dir() and pred(f))

    @staticmethod
    def get_files_by_path(path, pred=lambda f: True):
        """
        Returns all files of a given path.
        :param path: The path in which the files are searched.
        :param pred: The predicate to filter the files.
        :return: A list of all files in the given path.
        """
        return FileHelper.get_entries_by_path(path, lambda f: f.is_file() and pred(f))

    @staticmethod
    def get_entries_by_path(path, pred):
        """
        Returns all entries of a given path.
        :param path: The path in which the entries are searched.
        :param pred: The predicate to filter the entries.
        :return: A list of all entries in the given path.
        """
        return [f.path for f in os.scandir(path) if pred(f)]

    @staticmethod
    def exists(path):
        """
        Check if a file or directory exists.
        :param path: The path to check.
        :return: True if the file or directory exists, False otherwise.
        """
        return os.path.exists(path)

    @staticmethod
    def clear_directory(path):
        """
        Clear a directory by removing all files and directories.
        :param path: The path of the directory to clear.
        """
        if os.path.exists(path):
            shutil.rmtree(path)  # Löscht den gesamten Ordner samt Inhalt
            os.mkdir(path)  # Erstellt den Ordner erneut

    @staticmethod
    def get_file_name(path):
        return os.path.splitext(os.path.basename(path))[0]
