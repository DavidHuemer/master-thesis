from codeExecution.runtime.javaRuntimeTypeParser import JavaRuntimeTypeParser


class JavaRuntimeParameter:
    """
    Represents a java method parameter
    """

    def __init__(self, param):
        """
        Initializes a new JavaRuntimeParameter object
        :param param: The jpype parameter object
        """
        self.param = param

        self.parameter_name = JavaRuntimeTypeParser.get_correct_type(str(param.getName()))

    def __str__(self):
        return self.parameter_name
