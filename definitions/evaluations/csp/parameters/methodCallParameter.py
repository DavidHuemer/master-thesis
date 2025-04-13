class MethodCallParameter:
    def __init__(self, old_value, new_value=None):
        """

        :param old_value: The value of the parameter before the method call
        :param new_value: The value of the parameter after the method call
        """

        self.old_value = old_value
        self.new_value = new_value

    def __str__(self):
        if self.new_value:
            return f"{self.old_value} -> {self.new_value}"
        return str(self.old_value)
