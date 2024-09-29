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

        param_name = str(param.getName())
        if param_name == '[I':  # TODO: Add support for other array types
            param_name = 'int[]'

        self.parameter_name = param_name

    def __str__(self):
        return self.parameter_name
