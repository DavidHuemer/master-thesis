from definitions.ast.exceptionExpression import ExceptionExpression
from definitions.code.parameterExtractionInfo import ParameterExtractionInfo
from definitions.evaluations.tests.signalTestCollection import SignalTestCollection
from testGeneration.testCollections.jmlProblemBuilder import build_jml_problem
from testGeneration.testCaseGeneration.testCaseGenerator import generate_test_cases


def build_signal_test_collection(parameters: list[ParameterExtractionInfo],
                                 signals_conditions: list[ExceptionExpression]) \
        -> list[SignalTestCollection]:
    test_collections = []

    for signal in signals_conditions:
        jml_problem = build_jml_problem(parameters, [signal.expression])
        test_cases = generate_test_cases(jml_problem)
        test_collections.append(
            SignalTestCollection(test_cases, signal.exception_type, jml_problem.parameters.csp_parameters))

    return test_collections
