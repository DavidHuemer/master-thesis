import z3.z3num
from z3 import ForAll, Implies, And, Exists, ArithRef

from definitions.ast.quantifier.fullRangeTreeNode import FullRangeTreeNode
from definitions.ast.quantifier.numQuantifierTreeNode import NumQuantifierTreeNode
from definitions.ast.quantifier.numericQuantifierType import NumericQuantifierType
from definitions.evaluations.csp.jmlProblem import JMLProblem
from definitions.evaluations.csp.parameters.jmlParameters import JmlParameters
from verification.constraints.quantifier.quantifierRangeValuesHelper import QuantifierRangeValuesHelper
from verification.csp.cspParamNameGenerator import CspParamNameGenerator


class NumQuantifierRangeConstraintBuilder:
    def __init__(self, quantifier_range_values_helper=QuantifierRangeValuesHelper(),
                 name_generator=CspParamNameGenerator()):
        self.quantifier_range_values_helper = quantifier_range_values_helper
        self.name_generator = name_generator

    def evaluate(self, jml_problem: JMLProblem, parameters: JmlParameters, expression: NumQuantifierTreeNode,
                 expression_constraint_builder):
        from verification.constraints.expressionConstraintBuilder import ExpressionConstraintBuilder
        expression_constraint_builder: ExpressionConstraintBuilder = expression_constraint_builder

        if (expression.quantifier_type == NumericQuantifierType.SUM
                or expression.quantifier_type == NumericQuantifierType.PRODUCT):
            raise Exception("NumQuantifierConstraintBuilder: Sum and product quantifiers are not supported with range")

        csp_parameters, copied_parameters = self.quantifier_range_values_helper.handle_range_variables(expression,
                                                                                                       parameters)
        tmp_key = self.name_generator.find_name(copied_parameters.csp_parameters, "tmp")
        tmp_param = z3.Int(tmp_key)

        csp_values = [csp_param.value for csp_param in csp_parameters]
        range_expr = self.get_and(expression.range_, jml_problem, copied_parameters, expression_constraint_builder)

        result_expr = expression_constraint_builder.build_expression_constraint(jml_problem,
                                                                                copied_parameters,
                                                                                expression.expressions)
        comparison = self.get_comparison(tmp_param=tmp_param,
                                         result_expr=result_expr,
                                         quantifier_type=expression.quantifier_type)

        for_implies = Implies(range_expr, comparison)
        f = ForAll(csp_values, for_implies)

        exists_and = And(range_expr, tmp_param == result_expr)
        e = Exists(csp_values, exists_and)

        jml_problem.add_constraint(f)
        jml_problem.add_constraint(e)
        return tmp_param

    @staticmethod
    def get_comparison(tmp_param, result_expr, quantifier_type: NumericQuantifierType):
        if quantifier_type == NumericQuantifierType.MAX:
            return tmp_param >= result_expr
        elif quantifier_type == NumericQuantifierType.MIN:
            return tmp_param <= result_expr
        else:
            raise Exception("NumQuantifierRangeConstraintBuilder: Invalid quantifier type")

    def get_and(self, range_: FullRangeTreeNode, jml_problem: JMLProblem, jml_parameters: JmlParameters,
                expression_constraint_builder):
        from verification.constraints.expressionConstraintBuilder import ExpressionConstraintBuilder
        expression_constraint_builder: ExpressionConstraintBuilder = expression_constraint_builder

        range_list = []

        for r in range_.ranges:
            ident = jml_parameters.csp_parameters[r.name].value
            if not isinstance(ident, ArithRef):
                raise Exception("NumQuantifierRangeConstraintBuilder: Invalid range variable")

            start = expression_constraint_builder.build_expression_constraint(jml_problem, jml_parameters, r.start)
            end = expression_constraint_builder.build_expression_constraint(jml_problem, jml_parameters, r.end)
            range_list.append(self.get_single_range_and(ident, start, end, r.start_operator, r.end_operator))

        return And(*range_list)

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
