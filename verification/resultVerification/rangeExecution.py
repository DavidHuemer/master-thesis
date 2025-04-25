from contextlib import contextmanager

from z3 import sat, Or, ArrayRef, Not

from definitions.ast.astTreeNode import AstTreeNode
from definitions.code.parameterExtractionInfo import ParameterExtractionInfo
from definitions.evaluations.csp.cspParameter import CSPParameter
from helper.parameterHelper.parameterGenerator import get_parameters_by_parameter_extraction_infos
from testGeneration.testCaseGeneration.javaTypeMapper import get_python_from_java
from verification.csp.cspParamBuilder import build_csp_parameters
from verification.resultVerification.range.rangeBuilder import RangeBuilder
from verification.resultVerification.range.rangeProblem import RangeProblem
from verification.resultVerification.resultDto import ResultDto


class RangeExecution:
    def __init__(self, range_builder=None, quantifier_exec=None):
        self.range_builder = range_builder or RangeBuilder()

    @contextmanager
    def execute_range(self, range_: AstTreeNode, variables: list, t: ResultDto):
        """
        Updates the variables in t with the values from the range
        :param range_:
        :param variables:
        :param t:
        :return:
        """

        ranges = self.__execute_range(range_, variables, t)
        variable_infos = [ParameterExtractionInfo(variable[0], variable[1]) for variable in variables]
        range_var_names = [variable_info.name for variable_info in variable_infos]

        try:
            yield ranges
        finally:
            for var_name in range_var_names:
                if t.get_result_parameters().loop_parameters.exists(var_name):
                    t.get_result_parameters().loop_parameters.remove_parameter(var_name)

    def __execute_range(self, range_: AstTreeNode, variables: list, t: ResultDto):
        range_problem = RangeProblem()
        variable_infos = [ParameterExtractionInfo(variable[0], variable[1]) for variable in variables]
        range_var_names = [variable_info.name for variable_info in variable_infos]

        for method_call_parameter in t.get_result_parameters().method_call_parameters.get_parameter_list():
            method_call_param_constraint = method_call_parameter.get_constraint()
            range_problem.add_constraint(method_call_param_constraint)

        existing_loop_constraint = t.get_result_parameters().loop_parameters.get_and_constraints(use_old=True)
        range_problem.add_constraint(existing_loop_constraint)

        loop_params = get_parameters_by_parameter_extraction_infos(variable_infos)
        for loop_param in loop_params:
            t.get_result_parameters().loop_parameters.add_parameter(loop_param)

        new_t = t.copy_with_other_node(range_)
        constraint = self.range_builder.evaluate(new_t)
        range_problem.add_constraint(constraint)

        # ---------------

        # quantifier_csp_parameters = build_csp_parameters(variable_infos)
        #
        # for csp_param in t.get_result_parameters().csp_parameters.get_actual_parameters():
        #     if quantifier_csp_parameters.parameter_exists(csp_param.name):
        #         continue
        #
        #     quantifier_csp_parameters.add_csp_parameter(csp_param)
        #     method_param = t.get_result_parameters().get_parameter_by_key(csp_param.name, use_old=False, use_this=False)
        #
        #     if not isinstance(method_param, CSPParameter):
        #         method_param = get_python_from_java(method_param)
        #         range_problem.add_constraint(
        #             quantifier_csp_parameters[csp_param.name].is_null_param == (method_param is None))
        #
        #         if isinstance(csp_param.value, ArrayRef):
        #             for i in range(len(method_param)):
        #                 range_problem.add_constraint(csp_param.value[i] == method_param[i])
        #
        #             range_problem.add_constraint(
        #                 quantifier_csp_parameters[csp_param.name].length_param == len(method_param))
        #         else:
        #             range_problem.add_constraint(csp_param.value == method_param)
        #
        # # TODO: Instead of range_dto use result_dto
        #
        # for range_param in quantifier_csp_parameters.get_actual_parameters():
        #     if range_param.name in range_var_names and not t.get_result_parameters().csp_parameters.parameter_exists(
        #             range_param.name):
        #         t.get_result_parameters().csp_parameters.add_csp_parameter(range_param)
        #
        # # range_parameters = RangeParameters(t.get_result_parameters(), quantifier_csp_parameters)
        # # range_dto = RangeDto(node=range_, range_parameters=range_parameters, result=t.result)
        #
        # new_t = t.copy_with_other_node(range_)
        #
        # # Get constraint for solver
        # constraint = self.range_builder.evaluate(new_t)
        # range_problem.add_constraint(constraint)

        # for range_param in quantifier_csp_parameters.get_actual_parameters():
        #     if range_param.name in range_var_names and not t.get_result_parameters().csp_parameters.parameter_exists(
        #             range_param.name):
        #         t.get_result_parameters().csp_parameters.add_csp_parameter(range_param)

        counter = 0
        while range_problem.check() == sat and not t.stop_event.is_set():
            counter += 1
            if counter > 100000:
                print("More than 100000 iterations")

            model = range_problem.get_model()
            solution = dict()
            constraints = []

            # TODO: Evaluate loop parameters (add parameter to evaluate method to evaluate old state)
            t.get_result_parameters().loop_parameters.evaluate(model, use_old=True)
            loop_constraint = t.get_result_parameters().loop_parameters.get_and_constraints(True)
            range_problem.add_constraint(Not(loop_constraint))

            # for method_param in variable_infos:
            #     csp_param = quantifier_csp_parameters.get_parameter_by_key(method_param.name, False, False)
            #
            #     model_var = model[csp_param.value]
            #     solution[csp_param.name] = model_var.as_long()
            #     constraints.append(csp_param.value != model_var)
            #
            # or_constraint = Or(*constraints)
            # range_problem.add_constraint(or_constraint)
            #
            # for param_key in solution:
            #     t.get_result_parameters().local_parameters[param_key] = solution[param_key]

            yield t
