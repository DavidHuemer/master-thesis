class ParameterValue:
    """
    Represents the real value of a parameter (python and java value).
    """

    def __init__(self, python_value, java_value):
        self.python_value = python_value
        self.java_value = java_value
