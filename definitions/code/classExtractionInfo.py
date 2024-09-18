class ClassExtractionInfo:
    """
    Class to store information about a class that was extracted from a file.
    """

    def __init__(self, class_protection: str, class_name: str, code: str):
        """
        Constructor for the ClassExtractionInfo class.
        :param class_protection: The protection of the class.
        :param class_name: The name of the class.
        :param code: The code of the class.
        """
        self.class_protection = class_protection
        self.class_name = class_name
        self.code = code

    def __str__(self):
        return f'{self.class_name}'
