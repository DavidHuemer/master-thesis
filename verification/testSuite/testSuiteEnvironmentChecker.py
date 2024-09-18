from codeExecution.compilation.compilationEnvironmentChecker import CompilationEnvironmentChecker


class TestSuiteEnvironmentChecker:
    def __init__(self, compilation_environment_checker=CompilationEnvironmentChecker()):
        self.compilation_environment_checker = compilation_environment_checker

    def check_environment(self):
        """
        Check the environment for the test suite
        If the environment is not ready an exception is raised
        """
        self.compilation_environment_checker.check()
