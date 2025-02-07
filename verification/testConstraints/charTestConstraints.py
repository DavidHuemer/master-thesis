from z3 import Length, Range, InRe

from definitions.evaluations.csp.cspParameter import CSPParameter


class CharTestConstraintGenerator:
    @staticmethod
    def is_char(parameter: CSPParameter):
        return parameter.param_type == "char"

    @staticmethod
    def get_test_constraints(parameter: CSPParameter):
        yield Length(parameter.value) == 1

        allowed_chars = Range('A', 'A')
        yield InRe(parameter.value, allowed_chars)
