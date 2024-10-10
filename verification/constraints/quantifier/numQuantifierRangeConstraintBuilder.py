import z3.z3num
from z3 import ForAll, Implies, And, Exists, ArithRef

from definitions.ast.astTreeNode import AstTreeNode
from definitions.ast.quantifier.fullRangeTreeNode import FullRangeTreeNode
from definitions.ast.quantifier.numQuantifierTreeNode import NumQuantifierTreeNode
from definitions.ast.quantifier.numericQuantifierType import NumericQuantifierType
from verification.constraints.constraintsDto import ConstraintsDto
from verification.constraints.quantifier.quantifierRangeValuesHelper import QuantifierRangeValuesHelper
from verification.csp.cspParamNameGenerator import CspParamNameGenerator


class NumQuantifierRangeConstraintBuilder:
    def __init__(self, quantifier_range_values_helper=QuantifierRangeValuesHelper(),
                 name_generator=CspParamNameGenerator()):
        self.quantifier_range_values_helper = quantifier_range_values_helper
        self.name_generator = name_generator

    def evaluate(self, expression: NumQuantifierTreeNode, t: ConstraintsDto):
        if (expression.quantifier_type == NumericQuantifierType.SUM
                or expression.quantifier_type == NumericQuantifierType.PRODUCT):
            raise Exception("NumQuantifierConstraintBuilder: Sum and product quantifiers are not supported with range")

        csp_parameters = self.quantifier_range_values_helper.get_variables(expression)
        # TODO: Include csp and loop parameters
        tmp_key = self.name_generator.find_name(t.constraint_parameters, "tmp")
        tmp_param = z3.Int(tmp_key)

        for csp_param in csp_parameters:
            t.constraint_parameters.loop_parameters.add_csp_parameter(csp_param)

        csp_values = [csp_param.value for csp_param in csp_parameters]
        range_expr = t.constraint_builder.evaluate(t.copy_with_other_node(expression.range_))

        result_expr = t.constraint_builder.evaluate(t.copy_with_other_node(expression.expressions))
        comparison = self.get_comparison(tmp_param=tmp_param,
                                         result_expr=result_expr,
                                         quantifier_type=expression.quantifier_type)

        for_implies = Implies(range_expr, comparison)
        f = ForAll(csp_values, for_implies)

        exists_and = And(range_expr, tmp_param == result_expr)
        e = Exists(csp_values, exists_and)

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
