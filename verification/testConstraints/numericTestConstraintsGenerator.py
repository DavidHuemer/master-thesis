from definitions.evaluations.csp.cspParameter import CSPParameter
from verification.testConstraints.baseTestContraintsGenerator import BaseTestConstraintsGenerator


class NumericTestConstraintsGenerator(BaseTestConstraintsGenerator):
    """
    Helper class to generate numeric constraints for the parameters of a CSP.
    """

    def __init__(self):
        pass

    @staticmethod
    def is_numeric(parameter: CSPParameter) -> bool:
        """
        Return whether the parameter is numeric or not.
        :param parameter: The parameter to check.
        :return: True if the parameter is numeric, False otherwise.
        """
        return parameter.param_type in ["int", "long", "float", "double"]

    @staticmethod
    def get_test_constraints(parameter: CSPParameter):
        # TODO: Test with other values
        yield parameter.value < -100
        yield parameter.value < -20
        yield parameter.value < -10
        yield parameter.value < 0
        yield parameter.value == 0
        yield parameter.value > 0
        yield parameter.value > 10
        yield parameter.value > 20
        yield parameter.value > 100
