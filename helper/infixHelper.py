from typing import Callable

from z3 import And, Or, Not, ArrayRef, BoolRef

from definitions.evaluations.csp.parameters.cspParamHelperType import CSPParamHelperType
from definitions.evaluations.csp.parameters.cspParameters import CSPParameters


class InfixHelper:
    @staticmethod
    def evaluate_infix(infix_operator: str, csp_parameters: CSPParameters | None, left: Callable, right: Callable,
                       is_smt: bool):
        left_expr = left()

        if is_smt:
            right_expr = right()
            if isinstance(left_expr, ArrayRef) and isinstance(right_expr, BoolRef):
                # left_expr = get_param(is_null_name).value
                left_expr = csp_parameters.get_helper(str(left_expr), CSPParamHelperType.IS_NULL).value

            if isinstance(right_expr, ArrayRef) and isinstance(left_expr, BoolRef):
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

        if infix_operator == "+":
            return left_expr + right_expr
        elif infix_operator == "-":
            return left_expr - right_expr
        elif infix_operator == "*":
            return left_expr * right_expr
        elif infix_operator == "/":
            return left_expr / right_expr
        elif infix_operator == "&&":
            return And(left_expr, right_expr) if is_smt else left_expr and right()
        elif infix_operator == "||":
            return And(left_expr, right_expr) if is_smt else left_expr or right()
        elif infix_operator == "==":
            return left_expr == right_expr
        elif infix_operator == "<==>":
            return left_expr == right_expr
        elif infix_operator == "!=":
            return left_expr != right_expr
        elif infix_operator == "<=!=>":
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
