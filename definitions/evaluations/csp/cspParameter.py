import uuid

from z3 import ExprRef, ArrayRef, Bool, Int


class CSPParameter:
    def __init__(self, name: str, value: ExprRef, param_type: str, helper: bool = False):
        self.name = name
        self.value = value
        self.param_type = param_type
        self.is_helper = helper

        is_null_name = f"{name}_is_null_{uuid.uuid4()}"
        self.is_null_param = Bool(is_null_name)

        self.length_param = self.__build_length_param() if self.is_array() else None

    def __build_length_param(self):
        length_name = f"{self.name}_length_{uuid.uuid4()}"
        return Int(length_name)

    def __str__(self):
        return f"{self.param_type} {self.value}"

    def is_array(self):
        return isinstance(self.value, ArrayRef)

    def has_param(self, param_name: str):
        return (param_name in self.name or str(
            self.is_null_param) == param_name or
                (self.length_param is not None and str(self.length_param) == param_name))

    def __getitem__(self, key: str):
        if key == str(self.is_null_param):
            return self.is_null_param

        if self.length_param is not None and key == str(self.length_param):
            return self.length_param

        return None
