from definitions.code.javaTypeExtractionInfo import JavaTypeExtractionInfo


class ParameterExtractionInfo(JavaTypeExtractionInfo):
    """
    Class that holds information about the extraction of a parameter from a method. (type, name)
    """

    def __init__(self, parameter_type: str, name: str, dimension: int = 0):
        """
        Initializes the ParameterExtractionInfo object.
        :param parameter_type: The type of the parameter (e.g. int, String, etc.)
        :param name: The name of the parameter.
        """

        super().__init__(parameter_type, dimension)
        self.name = name

    def __eq__(self, other):
        return self.variable_type == other.variable_type and self.dimension == other.dimension and self.name == other.name

    def __str__(self):
        return f"{self.variable_type}{'[]' * self.dimension} {self.name}"
