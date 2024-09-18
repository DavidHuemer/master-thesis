class ParameterExtractionInfo:
    """
    Class that holds information about the extraction of a parameter from a method. (type, name)
    """

    def __init__(self, parameter_type: str, name: str):
        """
        Initializes the ParameterExtractionInfo object.
        :param parameter_type: The type of the parameter (e.g. int, String, etc.)
        :param name: The name of the parameter.
        """

        self.parameter_type = parameter_type
        self.name = name

    def __eq__(self, other):
        return self.parameter_type == other.parameter_type and self.name == other.name

    def __str__(self):
        return f"{self.parameter_type} {self.name}"
