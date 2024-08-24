class MethodExtractionInfo:
    """
    Class to store information about a method that was extracted from a file.
    """

    def __init__(self, comment, method_protection, method_return_type, method_name, method_parameters):
        """
        Constructor for the MethodExtractionInfo class.
        :param comment: The comment of the method.
        :param method_protection: The protection of the method.
        :param method_return_type: The return type of the method.
        :param method_name: The name of the method.
        :param method_parameters: The parameters of the method.
        """
        self.comment = comment
        self.method_protection = method_protection
        self.method_return_type = method_return_type
        self.method_name = method_name
        self.method_parameters = method_parameters

    def __eq__(self, other):
        return self.comment == other.comment and self.method_protection == other.method_protection and self.method_return_type == other.method_return_type and self.method_name == other.method_name and self.method_parameters == other.method_parameters

    def __str__(self):
        return f"{self.comment} {self.method_protection}"
