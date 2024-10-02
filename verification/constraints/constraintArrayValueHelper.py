from typing import Callable, Any

from z3 import ArrayRef, ExprRef, If, Implies, ArithRef, And, Int, ForAll, Exists

from definitions.ast.quantifier.numericQuantifierType import NumericQuantifierType
from definitions.config import MAX_ARRAY_SIZE
from definitions.evaluations.csp.cspParameter import CSPParameter
from definitions.evaluations.csp.jmlProblem import JMLProblem


class ConstraintArrayValueHelper:
    """
    Helper class for getting values from a constraint array
    """

    def __init__(self):
        pass

    def get_value_from_array(self, array: ArrayRef, length: CSPParameter,
                             quantifier_type: NumericQuantifierType, jml_problem: JMLProblem):

        length_value = length.value
        if not isinstance(length_value, ArithRef):
            raise Exception("Length value is not an ArithRef")

        if quantifier_type == NumericQuantifierType.MAX:
            return self.get_max(array, length_value)
        elif quantifier_type == NumericQuantifierType.MIN:
            return self.get_min(array, length_value, jml_problem)
        elif quantifier_type == NumericQuantifierType.SUM:
            pass
        elif quantifier_type == NumericQuantifierType.PRODUCT:
            pass

        raise Exception("Not implemented")

    def get_max(self, array, length):
        return self.get_matching_from_array(array, 0, length, lambda a, b: a >= b)

    def get_min(self, array: ArrayRef, length: ArithRef, jml_problem: JMLProblem):
        tmpMin = Int('tmpMin')
        i = Int('i')
        f = ForAll([i], Implies(And(i >= 0, i < length), tmpMin <= array[i]))
        e = Exists([i], And(i >= 0, i < length, tmpMin == array[i]))

        and_constraint = And(f, e)
        jml_problem.add_constraint(and_constraint)
        return tmpMin
        # return self.get_matching_from_array(array, 0, length, lambda a, b: a <= b)

    def get_sum(self, array, length):
        return self.get_computation_from_array(array, 0, length, lambda a, b: a + b, 0)

    def get_product(self, array, length):
        return self.get_computation_from_array(array, 0, length, lambda a, b: a * b, 1)

    def get_matching_from_array(self, array: ArrayRef, index: int, length: ArithRef,
                                comparison: Callable[[Any, Any], Any]):
        if index == 10:
            return 1 != 1

        return If(self.get_and_constraint(array, index, length, comparison), array[index],
                  self.get_matching_from_array(array, index + 1, length, comparison))

    @staticmethod
    def get_and_constraint(array: ArrayRef, index: int, length: ArithRef,
                           comparison: Callable[[ExprRef, ExprRef], ExprRef]):
        constraints = []
        for i in range(MAX_ARRAY_SIZE):
            implies = Implies(i < length, comparison(array[index], array[i]))
            constraints.append(implies)

        return And(index < length, *constraints)

    def get_computation_from_array(self, array: ArrayRef, index: int, length: ArithRef,
                                   computation: Callable[[ExprRef, ExprRef], ExprRef], default_value):
        if index == MAX_ARRAY_SIZE:
            return array[MAX_ARRAY_SIZE - 1]

        return If(index < length,
                  computation(array[index],
                              self.get_computation_from_array(array, index + 1, length, computation,
                                                              default_value)),
                  default_value)
