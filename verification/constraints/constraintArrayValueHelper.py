from typing import Callable, Any

from z3 import ArrayRef, ExprRef, Implies, ArithRef, And, Int, ForAll, Exists, Function, IntSort

from definitions.ast.quantifier.numericQuantifierType import NumericQuantifierType
from definitions.evaluations.csp.cspParameter import CSPParameter
from definitions.evaluations.csp.jmlProblem import JMLProblem
from definitions.evaluations.csp.parameters.cspParameters import CSPParameters
from definitions.evaluations.csp.parameters.jmlParameters import JmlParameters
from verification.csp.cspFunctionNameGenerator import CspFunctionNameGenerator
from verification.csp.cspParamNameGenerator import CspParamNameGenerator


class ConstraintArrayValueHelper:
    """
    Helper class for getting values from a constraint array
    """

    def __init__(self, name_generator=CspParamNameGenerator(), function_name_generator=CspFunctionNameGenerator()):
        self.name_generator = name_generator
        self.function_name_generator = function_name_generator

    def get_value_from_array(self, array: ArrayRef, length: CSPParameter,
                             quantifier_type: NumericQuantifierType, jml_problem: JMLProblem,
                             parameters: JmlParameters):

        length_value = length.value
        if not isinstance(length_value, ArithRef):
            raise Exception("Length value is not an ArithRef")

        if quantifier_type == NumericQuantifierType.MAX:
            return self.get_max(array, length_value, jml_problem, parameters.csp_parameters)
        elif quantifier_type == NumericQuantifierType.MIN:
            return self.get_min(array, length_value, jml_problem, parameters.csp_parameters)
        elif quantifier_type == NumericQuantifierType.SUM:
            return self.get_sum(array, length_value, jml_problem, parameters)
        elif quantifier_type == NumericQuantifierType.PRODUCT:
            return self.get_product(array, length_value, jml_problem, parameters)

        raise Exception("Not implemented")

    def get_max(self, array: ArrayRef, length: ArithRef, jml_problem: JMLProblem, csp_parameters: CSPParameters):
        return self.get_comparison(jml_problem, csp_parameters, array, length, lambda a, b: a >= b)

    def get_min(self, array: ArrayRef, length: ArithRef, jml_problem: JMLProblem, csp_parameters: CSPParameters):
        return self.get_comparison(jml_problem, csp_parameters, array, length, lambda a, b: a <= b)

    def get_comparison(self, jml_problem: JMLProblem, csp_parameters: CSPParameters, array: ArrayRef, length: ArithRef,
                       comparison: Callable[[ExprRef, ExprRef], Any]):

        i = Int('index')
        tmp_key = self.name_generator.find_name(csp_parameters, "tmp")
        tmp_param = CSPParameter(tmp_key, Int(tmp_key), 'int', True)
        csp_parameters.add_csp_parameter(tmp_param)

        f = ForAll([i], Implies(And(And(i >= 0, i < length)), comparison(tmp_param.value, array[i])))
        e = Exists([i], And(i >= 0, i < length, tmp_param.value == array[i]))

        jml_problem.add_constraint(f)
        jml_problem.add_constraint(e)

        return tmp_param

    def get_sum(self, array, length, jml_problem: JMLProblem, jml_parameters: JmlParameters):
        return self.get_computation(array, length, jml_problem, jml_parameters, 'sum', lambda a, b: a + b, 0)

    def get_product(self, array, length, jml_problem: JMLProblem, jml_parameters: JmlParameters):
        return self.get_computation(array, length, jml_problem, jml_parameters, 'product', lambda a, b: a * b, 1)

    def get_computation(self, array: ArrayRef, length, jml_problem: JMLProblem, jml_parameters: JmlParameters,
                        name: str,
                        computation: Callable[[ExprRef, ExprRef], ExprRef], default_value):
        function_name = self.function_name_generator.get_name(jml_parameters, name)

        f = Function(function_name, IntSort(), IntSort())
        jml_problem.add_constraint(f(-1) == default_value)

        i = Int('i')
        for_all = ForAll([i], Implies(And(i >= 0, i < length), f(i) == computation(f(i - 1), array[i])))
        result_key = self.name_generator.find_name(jml_parameters.csp_parameters, 'result')
        result_param = CSPParameter(result_key, Int(result_key), 'int', True)
        jml_parameters.csp_parameters.add_csp_parameter(result_param)
        jml_problem.add_constraint(for_all)
        jml_problem.add_constraint(result_param.value == f(length - 1))

        return result_param.value