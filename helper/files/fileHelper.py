import os


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
