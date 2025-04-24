from contextlib import contextmanager

from z3 import sat, Or, ArrayRef

from definitions.ast.astTreeNode import AstTreeNode
from definitions.code.parameterExtractionInfo import ParameterExtractionInfo
from definitions.evaluations.csp.parameters.rangeParameters import RangeParameters
from helper.logs.loggingHelper import log_info
from testGeneration.testCaseGeneration.javaTypeMapper import get_python_from_java
from verification.csp.cspParamBuilder import build_csp_parameters
from verification.resultVerification.range.rangeBuilder import RangeBuilder
from verification.resultVerification.range.rangeDto import RangeDto
from verification.resultVerification.range.rangeProblem import RangeProblem
from verification.resultVerification.resultDto import ResultDto


class RangeExecution:
    def __init__(self, range_builder=None, quantifier_exec=None):
        self.range_builder = range_builder or RangeBuilder(quantifier_range_execution=quantifier_exec)

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
                if t.get_result_parameters().csp_parameters.parameter_exists(var_name):
                    t.get_result_parameters().csp_parameters.remove_parameter(var_name)

            t.get_result_parameters().local_parameters.pop_var_names(range_var_names)

    def __execute_range(self, range_: AstTreeNode, variables: list, t: ResultDto):
        range_problem = RangeProblem()
        variable_infos = [ParameterExtractionInfo(variable[0], variable[1]) for variable in variables]
        range_var_names = [variable_info.name for variable_info in variable_infos]

        quantifier_csp_parameters = build_csp_parameters(variable_infos)

        for csp_param in t.get_result_parameters().csp_parameters.get_actual_parameters():
            if quantifier_csp_parameters.parameter_exists(csp_param.name):
                continue

            quantifier_csp_parameters.add_csp_parameter(csp_param)
            method_param = t.get_result_parameters().get_parameter_by_key(csp_param.name, use_old=False, use_this=False)

            method_param = get_python_from_java(method_param)
            range_problem.add_constraint(
                quantifier_csp_parameters[csp_param.name].is_null_param == (method_param is None))

            if isinstance(csp_param.value, ArrayRef):
                for i in range(len(method_param)):
                    range_problem.add_constraint(csp_param.value[i] == method_param[i])

                range_problem.add_constraint(
                    quantifier_csp_parameters[csp_param.name].length_param == len(method_param))
            else:
                range_problem.add_constraint(csp_param.value == method_param)

        range_parameters = RangeParameters(t.get_result_parameters(), quantifier_csp_parameters)
        range_dto = RangeDto(node=range_, range_parameters=range_parameters, result=t.result)

        # Get constraint for solver
        constraint = self.range_builder.evaluate(range_dto)
        range_problem.add_constraint(constraint)

        for range_param in quantifier_csp_parameters.get_actual_parameters():
            if range_param.name in range_var_names and not t.get_result_parameters().csp_parameters.parameter_exists(
                    range_param.name):
                t.get_result_parameters().csp_parameters.add_csp_parameter(range_param)

        counter = 0
        while range_problem.check() == sat and not t.stop_event.is_set():
            counter += 1
            if counter > 100000:
                print("More than 100000 iterations")

            model = range_problem.get_model()
            solution = dict()
            constraints = []

            for method_param in variable_infos:
                csp_param = quantifier_csp_parameters.get_parameter_by_key(method_param.name, False, False)

                model_var = model[csp_param.value]
                solution[csp_param.name] = model_var.as_long()
                constraints.append(csp_param.value != model_var)

            or_constraint = Or(*constraints)
            range_problem.add_constraint(or_constraint)

            for param_key in solution:
                t.get_result_parameters().local_parameters[param_key] = solution[param_key]

            yield t
