import os

from codetiming import Timer

from definitions import compilationConfig
from definitions.codeExecution.compilation.CompilationException import CompilationException
from definitions.javaCode import JavaCode
from helper.files.fileHelper import FileHelper
from helper.logs.loggingHelper import log_info
from helper.processHelper import run_command

compilation_timer = Timer(name="compilation", logger=None)


@compilation_timer
def compile_java_files(java_files: list[str]):
    log_info(f"Starting Java compilation ({len(java_files)} files)")
    check_dist_folder()
    run_command(["javac", "-d", compilationConfig.DIST_FOLDER, *java_files])
    log_info("Java compilation successful")


def check_java_file(java_code: JavaCode):
    if not FileHelper.exists(java_code.file_path):
        raise CompilationException(f"Java file not found at {java_code.file_path}")

    # Check that the file has the same name as the class
    file_name = FileHelper.get_file_name(java_code.file_path)

    if file_name != java_code.class_name:
        raise CompilationException(
            f"File name {file_name} does not match class name {java_code.class_name}")


def check_dist_folder():
    if FileHelper.exists(compilationConfig.DIST_FOLDER):
        FileHelper.clear_directory(compilationConfig.DIST_FOLDER)
        pass
    else:
        os.mkdir(compilationConfig.DIST_FOLDER)


def check_verification(java_code: JavaCode):
    expected_class_path = os.path.join(compilationConfig.DIST_FOLDER, java_code.class_name + ".class")
    if not FileHelper.exists(expected_class_path):
        raise CompilationException(f"Class file not found at {expected_class_path}")
