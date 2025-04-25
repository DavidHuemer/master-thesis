import uuid

from z3 import BoolRef, Bool

from definitions.parameters.parameter import Parameter


class SpecialParameters:
    def __init__(self, is_null_param: BoolRef | None = None, result_parameter: Parameter | None = None):
        self.is_null_param = is_null_param or Bool(f"is_null_{uuid.uuid4()}")
        self.result_parameter: Parameter | None = None
