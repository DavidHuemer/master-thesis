from unittest import TestCase

from parameterized import parameterized
from z3 import ArithRef, ArrayRef, BoolRef, SeqRef

from definitions.code.parameterExtractionInfo import ParameterExtractionInfo
from verification.csp.cspParamBuilder import CSPParameterBuilder


class TestCSPParameterBuilder(TestCase):

    def setUp(self):
        super().setUp()
        self.builder = CSPParameterBuilder()

    @parameterized.expand([
        ("byte", "a", ArithRef),
        ("byte[]", "arr", ArrayRef),
        ("short", "a", ArithRef),
        ("short[]", "arr", ArrayRef),
        ("int", "a", ArithRef),
        ("int[]", "arr", ArrayRef),
        ("long", "b", ArithRef),
        ("long[]", "arr", ArrayRef),
        ("float", "c", ArithRef),
        ("float[]", "arr", ArrayRef),
        ("double", "d", ArithRef),
        ("double[]", "arr", ArrayRef),
        ("boolean", "e", BoolRef),
        ("boolean[]", "arr", ArrayRef),
        ("char", "c", SeqRef),
        ("char[]", "arr", ArrayRef),
        ("String", "s", SeqRef),
        ("String[]", "arr", ArrayRef),
    ])
    def test_add(self, param_type: str, param_name: str, expected):
        param = ParameterExtractionInfo(param_type, param_name)
        result = self.builder.get_csp_param_for_param(param)

        if isinstance(result, ArithRef):
            print("Test")

        self.assertIsInstance(result.value, expected,
                              "The result should be an instance of the expected type")

        self.assertEqual(result.name, param_name,
                         "The name should be the same as the parameter name")

        self.assertEqual(str(result.value), param_name,
                         "The name of the z3 variable should be the same as the parameter name")
