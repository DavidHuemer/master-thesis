from typing import Callable

from jpype import java, JChar, JDouble
from z3 import And, Or, Not, ArrayRef, BoolRef, SeqRef, CharVal, CharRef

from definitions.evaluations.csp.parameters.cspParamHelperType import CSPParamHelperType
from definitions.evaluations.csp.parameters.cspParameters import CSPParameters


class InfixHelper:
    def evaluate_infix(self, infix_operator: str, csp_parameters: CSPParameters | None, left: Callable, right: Callable,
                       is_smt: bool):
        left_expr = left()

        if is_smt:
            right_expr = right()
            if (isinstance(left_expr, ArrayRef) or isinstance(left_expr, SeqRef)) and isinstance(right_expr, BoolRef):
                # left_expr = get_param(is_null_name).value
                left_expr = csp_parameters.get_helper(str(left_expr), CSPParamHelperType.IS_NULL).value

            if (isinstance(right_expr, ArrayRef) or isinstance(right_expr, SeqRef)) and isinstance(left_expr, BoolRef):
                # is_null_name = f"{str(right_expr)}_is_null"
                right_expr = csp_parameters.get_helper(str(right_expr), CSPParamHelperType.IS_NULL).value
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
                    return left_expr == CharVal(right_expr)

                return left_expr == right_expr

            if self.is_float(left_expr) or self.is_float(right_expr):
                return self.evaluate_float(left_expr, right_expr)

            return left_expr == right_expr
        elif infix_operator == "!=" or infix_operator == "<=!=>":
            if is_smt:
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
