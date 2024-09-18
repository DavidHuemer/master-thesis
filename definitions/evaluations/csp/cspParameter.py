class CSPParameter:
    def __init__(self, name, value, param_type: str, helper: bool = False):
        self.name = name
        self.value = value
        self.param_type = param_type
        self.is_helper = helper

    def __str__(self):
        return f"{self.param_type} {self.value}"

    def is_array(self):
        return self.param_type.endswith("[]")
