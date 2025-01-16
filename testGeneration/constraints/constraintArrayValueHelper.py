from typing import Callable, Any

from z3 import ArrayRef, ExprRef, Implies, ArithRef, And, Int, ForAll, Exists, Function, IntSort

from definitions.ast.quantifier.numericQuantifierType import NumericQuantifierType
from definitions.evaluations.csp.cspParameter import CSPParameter
from testGeneration.constraints.constraintsDto import ConstraintsDto
from verification.csp.cspFunctionNameGenerator import CspFunctionNameGenerator
from verification.csp.cspParamNameGenerator import find_csp_name


class ConstraintArrayValueHelper:
    """
    Helper class for getting values from a constraint array
    """

    def __init__(self, function_name_generator=CspFunctionNameGenerator()):
        self.function_name_generator = function_name_generator

    def get_value_from_array(self, array: ArrayRef, length: CSPParameter,
                             quantifier_type: NumericQuantifierType, t: ConstraintsDto):

        length_value = length.value
        if not isinstance(length_value, ArithRef):
            raise Exception("Length value is not an ArithRef")

        if quantifier_type == NumericQuantifierType.MAX:
            return self.get_max(array, length_value, t)
        elif quantifier_type == NumericQuantifierType.MIN:
            return self.get_min(array, length_value, t)
        elif quantifier_type == NumericQuantifierType.SUM:
            return self.get_sum(array, length_value, t)
        elif quantifier_type == NumericQuantifierType.PRODUCT:
            return self.get_product(array, length_value, t)

        raise Exception("Not implemented")

    def get_max(self, array: ArrayRef, length: ArithRef, t: ConstraintsDto):
        return self.get_comparison(t, array, length, lambda a, b: a >= b)

    def get_min(self, array: ArrayRef, length: ArithRef, t: ConstraintsDto):
        return self.get_comparison(t, array, length, lambda a, b: a <= b)

    def get_comparison(self, t: ConstraintsDto, array: ArrayRef, length: ArithRef,
                       comparison: Callable[[ExprRef, ExprRef], Any]):

        i = Int('index')
        tmp_key = find_csp_name(t.constraint_parameters, "tmp")
        tmp_param = CSPParameter(tmp_key, Int(tmp_key), 'int', True)
        t.constraint_parameters.loop_parameters.add_csp_parameter(tmp_param)

        f = ForAll([i], Implies(And(And(i >= 0, i < length)), comparison(tmp_param.value, array[i])))
        e = Exists([i], And(i >= 0, i < length, tmp_param.value == array[i]))

        t.jml_problem.add_constraint(f)
        t.jml_problem.add_constraint(e)

        return tmp_param

    def get_sum(self, array, length, t: ConstraintsDto):
        return self.get_computation(array, length, t, 'sum', lambda a, b: a + b, 0)

    def get_product(self, array, length, t: ConstraintsDto):
        return self.get_computation(array, length, t, 'product', lambda a, b: a * b, 1)

    def get_computation(self, array: ArrayRef, length, t: ConstraintsDto,
                        name: str,
                        computation: Callable[[ExprRef, ExprRef], ExprRef], default_value):
        function_name = self.function_name_generator.get_name(t.constraint_parameters.functions, name)

        f = Function(function_name, IntSort(), IntSort())
        t.jml_problem.add_constraint(f(-1) == default_value)

        i = Int('i')
        for_all = ForAll([i], Implies(And(i >= 0, i < length), f(i) == computation(f(i - 1), array[i])))
        result_key = find_csp_name(t.constraint_parameters, 'result')
        result_param = CSPParameter(result_key, Int(result_key), 'int', True)
        t.constraint_parameters.csp_parameters.add_csp_parameter(result_param)
        t.jml_problem.add_constraint(for_all)
        t.jml_problem.add_constraint(result_param.value == f(length - 1))

        return result_param.value
