import os
import re

import jpype

from helper.files.fileHelper import FileHelper


class JvmPathHelper:
    """
    Helper class for handling the path to the JVM.
    """

    def __init__(self, jvm=jpype, file_helper=FileHelper):
        self.jvm = jvm
        self.file_helper = file_helper

    def get_jvm_path(self):
        """
        Returns the JVM path.
        :return: The JVM path.
        """
        java_directory_path = self.get_java_directory_path()
        java_directories = os.listdir(java_directory_path)
        max_version = 0
        max_jvm_path = None

        for java_directory in java_directories:
            jvm_path = self.get_jvm_path_from_directory(java_directory, java_directory_path)
            version = self.get_version_from_directory(java_directory)
            if version and self.file_helper.exists(jvm_path) and version > max_version:
                max_version = version
                max_jvm_path = jvm_path

        if max_jvm_path is None:
            max_jvm_path = self.jvm.getDefaultJVMPath()

        if max_jvm_path is None or not self.file_helper.exists(max_jvm_path):
            raise Exception("Could not find JVM path")

        return max_jvm_path

    @staticmethod
    def get_java_directory_path():
        """
        Returns the location of the Java directory.
        :return: The location of the Java directory.
        """
        program_files = JvmPathHelper.get_program_files_path()
        return os.path.join(program_files, "Java")

    @staticmethod
    def get_program_files_path():
        """
        Returns the location of the Program Files directory.
        :return:
        """
        return os.environ['ProgramFiles']

    @staticmethod
    def get_jvm_path_from_directory(java_directory, java_directory_path):
        """
        Returns the JVM path from the given Java directory.
        :param java_directory: The name of a specific Java directory.
        :param java_directory_path: The path to the Java directory. (e.g. C:\\Program Files\\Java)
        :return: The JVM path.
        """
        jvm_path = os.path.join(java_directory_path, java_directory, "bin", "server", "jvm.dll")
        return jvm_path

    @staticmethod
    def get_version_from_directory(java_directory):
        """
        Returns the version of the Java directory.
        :param java_directory: The name of a specific Java directory.
        :return: The version of the Java directory.
        """
        java_directory_name_regex = r"(?P<test>jdk|jre)-(?P<version>\d+(?:\.\d+)?)"
        match = re.match(java_directory_name_regex, java_directory)
        if match:
            version = match.group("version")
            if version.isnumeric():
                return float(version)
        return None
