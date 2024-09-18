import os

from definitions import compilationConfig
from definitions.codeExecution.compilation.CompilationException import CompilationException
from definitions.javaCode import JavaCode
from helper.files.fileHelper import FileHelper
from helper.processHelper import ProcessHelper


class JavaCompilationRunner:
    def __init__(self, file_helper=FileHelper, process_helper=ProcessHelper):
        self.file_helper = file_helper
        self.process_helper = process_helper

    def compile(self, java_code: JavaCode):
        # Steps to compile the Java source code:

        # 1. Check the dist folder
        self.check_dist_folder()

        # 2. Check the Java File
        self.check_java_file(java_code)

        # 3. Compile the Java source code
        self.run_command(java_code)

        # 4. Check if the compilation is successful
        self.check_verification(java_code)

    def check_java_file(self, java_code: JavaCode):
        if not self.file_helper.exists(java_code.file_path):
            raise CompilationException(f"Java file not found at {java_code.file_path}")

        # Check that the file has the same name as the class
        file_name = self.file_helper.get_file_name(java_code.file_path)

        if file_name != java_code.class_info.class_name:
            raise CompilationException(
                f"File name {file_name} does not match class name {java_code.class_info.class_name}")

    def run_command(self, java_code):
        self.process_helper.run_command(["javac", "-d", compilationConfig.DIST_FOLDER, java_code.file_path])

    def check_dist_folder(self):
        if self.file_helper.exists(compilationConfig.DIST_FOLDER):
            self.file_helper.clear_directory(compilationConfig.DIST_FOLDER)
            pass
        else:
            os.mkdir(compilationConfig.DIST_FOLDER)

    def check_verification(self, java_code: JavaCode):
        expected_class_path = os.path.join(compilationConfig.DIST_FOLDER, java_code.class_info.class_name + ".class")
        if not self.file_helper.exists(expected_class_path):
            raise CompilationException(f"Class file not found at {expected_class_path}")
