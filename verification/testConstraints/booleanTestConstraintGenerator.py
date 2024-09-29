from definitions.evaluations.csp.cspParameter import CSPParameter


class BooleanTestConstraintGenerator:
    def __init__(self):
        pass

    @staticmethod
    def is_boolean(parameter):
        return parameter.param_type == "boolean"

    def get_test_constraints(self, parameter: CSPParameter):
        yield parameter.value == True
        yield parameter.value == False
