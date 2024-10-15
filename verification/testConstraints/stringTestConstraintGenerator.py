from z3 import Length

from definitions.evaluations.csp.cspParameter import CSPParameter


class StringTestConstraintGenerator:
    @staticmethod
    def is_string(parameter: CSPParameter):
        return parameter.param_type == "String"

    @staticmethod
    def get_test_constraints(parameter: CSPParameter):
        yield Length(parameter.value) == 0
        yield Length(parameter.value) > 0
        yield Length(parameter.value) > 5
        yield Length(parameter.value) > 10
