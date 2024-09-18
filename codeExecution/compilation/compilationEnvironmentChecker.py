from definitions.codeExecution.compilation.CompilationException import CompilationException
from helper.processHelper import ProcessHelper


class CompilationEnvironmentChecker:
    """
    Class that checks the environment if java compilation is possible
    """

    def __init__(self, process_helper=ProcessHelper):
        self.process_helper = process_helper

    def check(self):
        """
        Check the environment for the java compiler
        :return:
        """
        self.check_java_compiler_is_installed()

    def check_java_compiler_is_installed(self):
        """
        Check if the java compiler is installed
        :return: True if the java compiler is installed
        """
        if not self.process_helper.check_with_commands(["javac", "--version"]):
            raise CompilationException("Compiler not found")
