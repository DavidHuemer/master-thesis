import time

from z3 import sat, Or, ArrayRef

from definitions.ast.astTreeNode import AstTreeNode
from definitions.code.parameterExtractionInfo import ParameterExtractionInfo
from definitions.evaluations.csp.parameters.cspParamHelperType import CSPParamHelperType
from definitions.evaluations.csp.parameters.rangeParameters import RangeParameters
from verification.csp.cspParamBuilder import build_csp_parameters
from verification.resultVerification.range.rangeBuilder import RangeBuilder
from verification.resultVerification.range.rangeDto import RangeDto
from verification.resultVerification.range.rangeProblem import RangeProblem
from verification.resultVerification.resultDto import ResultDto


class RangeExecution:
    def __init__(self, range_builder=RangeBuilder()):
        self.range_builder = range_builder

    def execute_range(self, range_: AstTreeNode, variables: list, t: ResultDto):
        range_problem = RangeProblem()
        variable_infos = [ParameterExtractionInfo(variable[0], variable[1]) for variable in variables]

        quantifier_csp_parameters = build_csp_parameters(variable_infos)

        for csp_param in t.get_result_parameters().csp_parameters.get_actual_parameters():
            if quantifier_csp_parameters.parameter_exists(csp_param.name):
                continue

            quantifier_csp_parameters.add_csp_parameter(csp_param)
            method_param = t.get_result_parameters().method_call_parameters.get_parameter_by_key(csp_param.name, False,
                                                                                                 False)
            if isinstance(csp_param.value, ArrayRef):
                for i in range(len(method_param)):
                    range_problem.add_constraint(csp_param.value[i] == method_param[i])
            else:
                range_problem.add_constraint(csp_param.value == method_param)

            helpers = t.get_result_parameters().csp_parameters.get_helper_list_for_parameter(csp_param.name)

            for helper in helpers:
                csp_helper_key = t.get_result_parameters().csp_parameters.helper_parameters[helper]
                csp_helper = t.get_result_parameters().csp_parameters[csp_helper_key]
                quantifier_csp_parameters.add_helper_parameter(csp_param.name, helper[1], csp_helper)

                if helper[1] == CSPParamHelperType.LENGTH:
                    range_problem.add_constraint(csp_helper.value == len(method_param))

        range_parameters = RangeParameters(t.get_result_parameters(), quantifier_csp_parameters)
        range_dto = RangeDto(node=range_, range_parameters=range_parameters, constraint_builder=self.range_builder,
                             result=t.result)

        # Get constraint for solver
        constraint = self.range_builder.evaluate(range_dto)
        range_problem.add_constraint(constraint)

        solutions = []

        start_time = time.time()

        while range_problem.check() == sat and not t.stop_event.is_set():
            model = range_problem.get_model()
            solution = dict()
            constraints = []

            for method_param in variable_infos:
                csp_param = quantifier_csp_parameters.get_parameter_by_key(method_param.name, False, False)

                model_var = model[csp_param.value]
                solution[csp_param.name] = model_var.as_long()
                constraints.append(csp_param.value != model_var)
            solutions.append(solution)
            or_constraint = Or(*constraints)
            range_problem.add_constraint(or_constraint)

        for solution in solutions:
            for param_key in solution:
                range_parameters.result_parameters.local_parameters[param_key] = solution[param_key]

            yield t
        # range_expr: RangeTreeNode = ranges[0]
        # start = t.result_verifier.evaluate(t.copy_with_other_node(range_expr.start))
        # if range_expr.start_operator == "<":
        #     start += 1
        #
        # end = t.result_verifier.evaluate(t.copy_with_other_node(range_expr.end))
        # if range_expr.end_operator == "<=":
        #     end += 1
        #
        # for i in range(start, end):
        #     # result_copy = copy.deepcopy(result)
        #     # result_copy.parameters[range_expr.name] = i
        #
        #     t.result_parameters.local_parameters[range_expr.name] = i
        #
        #     if len(ranges) == 1:
        #         if range_.expr is not None:
        #             if t.result_verifier.evaluate(t.copy_with_other_node(range_.expr)):
        #                 yield t
        #
        #             # if result_verifier.evaluate(result_copy, range_.expr):
        #             #     yield result_copy
        #         else:
        #             yield t
        #     else:
        #         for r in self.execute_range(range_, ranges[1:], t):
        #             yield r
