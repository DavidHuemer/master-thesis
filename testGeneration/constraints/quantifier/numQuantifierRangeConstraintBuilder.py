import uuid

import z3.z3num
from z3 import ForAll, Implies, And, Exists, ArithRef

from definitions.ast.quantifier.numQuantifierTreeNode import NumQuantifierTreeNode
from definitions.ast.quantifier.numericQuantifierType import NumericQuantifierType
from nodes.baseNodeHandler import BaseNodeHandler
from testGeneration.constraints.constraintsDto import ConstraintsDto
from testGeneration.constraints.quantifier.quantifierRangeValuesHelper import QuantifierRangeValuesHelper
from verification.csp.cspParamNameGenerator import find_csp_name


class NumQuantifierRangeConstraintBuilder(BaseNodeHandler[ConstraintsDto]):
    def __init__(self, quantifier_range_values_helper=QuantifierRangeValuesHelper()):
        super().__init__()
        self.quantifier_range_values_helper = quantifier_range_values_helper

    def evaluate(self, expression: NumQuantifierTreeNode, t: ConstraintsDto):
        if (expression.quantifier_type == NumericQuantifierType.SUM
                or expression.quantifier_type == NumericQuantifierType.PRODUCT):
            raise Exception("NumQuantifierConstraintBuilder: Sum and product quantifiers are not supported with range")

        csp_parameters = self.quantifier_range_values_helper.get_variables(expression)
        # TODO: Include csp and loop parameters
        tmp_param = z3.Int(f"tmp_{uuid.uuid4()}")

        for csp_param in csp_parameters:
            t.constraint_parameters.loop_parameters.add_csp_parameter(csp_param)

        csp_values = [csp_param.value for csp_param in csp_parameters]
        range_expr = self.evaluate_with_runner(t, expression.range_)

        value_expression = self.evaluate_with_runner(t, expression.expressions)
        comparison = self.get_comparison(tmp_param=tmp_param,
                                         result_expr=value_expression,
                                         quantifier_type=expression.quantifier_type)

        f = ForAll(csp_values, Implies(range_expr, comparison))
        e = Exists(csp_values, And(range_expr, tmp_param == value_expression))

        t.jml_problem.add_constraint(f)
        t.jml_problem.add_constraint(e)
        return tmp_param

    @staticmethod
    def get_comparison(tmp_param, result_expr, quantifier_type: NumericQuantifierType):
        if quantifier_type == NumericQuantifierType.MAX:
            return tmp_param >= result_expr
        elif quantifier_type == NumericQuantifierType.MIN:
            return tmp_param <= result_expr
        else:
            raise Exception("NumQuantifierRangeConstraintBuilder: Invalid quantifier type")

    def get_single_range_and(self, ident: ArithRef, start, end, start_op: str, end_op: str):
        start = self.get_start_constraint(ident, start, start_op)

        end = self.get_end_constraint(end, end_op, ident)

        return And(start, end)

    @staticmethod
    def get_start_constraint(ident: ArithRef, start, start_op: str):
        if start_op == "<=":
            start = start <= ident
        elif start_op == "<":
            start = start < ident
        else:
            raise Exception("NumQuantifierRangeConstraintBuilder: Invalid start operator")
        return start

    @staticmethod
    def get_end_constraint(end, end_op: str, ident: ArithRef):
        if end_op == "<=":
            end = ident <= end
        elif end_op == "<":
            end = ident < end
        else:
            raise Exception("NumQuantifierRangeConstraintBuilder: Invalid end operator")
        return end
