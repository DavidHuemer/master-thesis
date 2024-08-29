class ExpectedResult:
    """
    This class is used to store the expected result of a method in a file.
    """

    def __init__(self, file_path, method_name, expected_result):
        """
        Initializes the ExpectedResult object
        :param file_path: The file path of the java file
        :param method_name: The name of the method
        :param expected_result: The expected result of the method
        """

        self.file_path = file_path
        self.method_name = method_name
        self.expected_result = expected_result

    def __str__(self):
        return f"{self.file_path}  =>  {self.method_name}={self.expected_result})"

    def __eq__(self, other):
        return (self.file_path == other.file_path
                and self.method_name == other.method_name
                and self.expected_result == other.expected_result)
