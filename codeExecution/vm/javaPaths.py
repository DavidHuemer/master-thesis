import os
import re
import jpype
from helper.files.fileHelper import FileHelper


def get_jvm_path() -> str:
    java_directory_path = get_java_directory_path()
    java_directories = os.listdir(java_directory_path)
    max_version = 0
    max_jvm_path = None

    for java_directory in java_directories:
        jvm_path = get_jvm_path_from_directory(java_directory, java_directory_path)
        version = get_version_from_directory(java_directory)
        if version and FileHelper.exists(jvm_path) and version > max_version:
            max_version = version
            max_jvm_path = jvm_path

    if not max_jvm_path:
        max_jvm_path = jpype.getDefaultJVMPath()

    if not max_jvm_path or not FileHelper.exists(max_jvm_path):
        raise Exception("Could not find JVM path")

    return max_jvm_path


def get_java_directory_path() -> str:
    return os.path.join(os.environ['ProgramFiles'], "Java")


def get_jvm_path_from_directory(java_directory: str, java_directory_path: str) -> str:
    return os.path.join(java_directory_path, java_directory, "bin", "server", "jvm.dll")


def get_version_from_directory(java_directory: str) -> float | None:
    match = re.match(r"(jdk|jre)-(\d+(?:\.\d+)?)", java_directory)
    return float(match.group(2)) if match else None