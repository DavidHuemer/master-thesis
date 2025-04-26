from typing import Callable

from jpype import JDouble
from z3 import And, Or, Not, BoolRef, SeqRef, CharVal, CharRef

from definitions.evaluations.csp.cspParameter import CSPParameter
from definitions.parameters.Variables import Variables
from helper.z3Helper import get_z3_value


class InfixHelper:
    def evaluate_infix(self, infix_operator: str, variables: Variables | None, left: Callable, right: Callable,
                       is_smt: bool):
        left_expr = left()

        if is_smt:
            right_expr = right()
            if ((isinstance(left_expr, CSPParameter) and not isinstance(left_expr.value, BoolRef))
                    and isinstance(get_z3_value(right_expr), BoolRef)):
                left_expr = left_expr.is_null_param

            if ((isinstance(right_expr, CSPParameter) and not isinstance(right_expr.value, BoolRef))
                    and isinstance(get_z3_value(left_expr), BoolRef)):
                right_expr = right_expr.is_null_param
        else:
            if infix_operator == "==>" and not left_expr:
                return True

            if infix_operator == "&&" and not left_expr:
                return False

            if infix_operator == "||" and left_expr:
                return True

            right_expr = right()

            if infix_operator == "==" and isinstance(left_expr, list):
                return left_expr is right_expr

            if infix_operator == "!=" and isinstance(left_expr, list):
                return left_expr is not right_expr

        left_expr = get_z3_value(left_expr)
        right_expr = get_z3_value(right_expr)

        if infix_operator == "+":
            return left_expr + right_expr
        elif infix_operator == "-":
            return left_expr - right_expr
        elif infix_operator == "*":
            return left_expr * right_expr
        elif infix_operator == "/":
            if isinstance(left_expr, int) and isinstance(right_expr, int):
                return int(left_expr / right_expr)
            return left_expr / right_expr
        elif infix_operator == "%":
            return left_expr % right_expr
        elif infix_operator == "&&":
            return And(left_expr, right_expr) if is_smt else left_expr and right()
        elif infix_operator == "||":
            return Or(left_expr, right_expr) if is_smt else left_expr or right()
        elif infix_operator == "==" or infix_operator == "<==>":
            if is_smt:
                if isinstance(left_expr, CharRef):
                    if isinstance(right_expr, SeqRef):
                        return left_expr == right_expr[0]

                    return left_expr == CharVal(right_expr)

                return left_expr == right_expr

            if self.is_float(left_expr) or self.is_float(right_expr):
                return self.evaluate_float(left_expr, right_expr)

            return left_expr == right_expr
        elif infix_operator == "!=" or infix_operator == "<=!=>":
            if is_smt:
                if isinstance(left_expr, CharRef):
                    if isinstance(right_expr, SeqRef):
                        return left_expr != right_expr[0]

                    return left_expr != CharVal(right_expr)

                return left_expr != right_expr

            if self.is_float(left_expr) or self.is_float(right_expr):
                return not self.evaluate_float(left_expr, right_expr)

            return left_expr != right_expr
        elif infix_operator == "==>":
            return Or(Not(left_expr), right_expr) if is_smt else (not left_expr) or right()
        elif infix_operator == "<":
            return left_expr < right_expr
        elif infix_operator == "<=":
            return left_expr <= right_expr
        elif infix_operator == ">":
            return left_expr > right_expr
        elif infix_operator == ">=":
            return left_expr >= right_expr

        raise Exception("Infix expression not supported")

    @staticmethod
    def is_float(expr):
        return isinstance(expr, float) or isinstance(expr, JDouble)

    @staticmethod
    def evaluate_float(left, right):
        return abs(left - right) < 0.000001
