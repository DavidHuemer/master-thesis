class ParameterExtractionInfo:
    """
    Class that holds information about the extraction of a parameter from a method. (type, name)
    """

    def __init__(self, parameter_type: str, name: str, dimension: int = 0):
        """
        Initializes the ParameterExtractionInfo object.
        :param parameter_type: The type of the parameter (e.g. int, String, etc.)
        :param name: The name of the parameter.
        """

        self.parameter_type = parameter_type
        self.full_parameter_type = parameter_type if dimension == 0 else f"{parameter_type}[]"
        self.name = name
        self.dimension = dimension

    def __eq__(self, other):
        return self.parameter_type == other.parameter_type and self.name == other.name

    def __str__(self):
        return f"{self.parameter_type}{'[]' * self.dimension} {self.name}"

    def is_array(self) -> bool:
        return self.dimension > 0
