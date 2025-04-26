from definitions.ast.exceptionExpression import ExceptionExpression
from definitions.evaluations.tests.signalTestCollection import SignalTestCollection
from definitions.parameters.Variables import Variables
from testGeneration.testCollections.jmlProblemBuilder import build_jml_problem
from testGeneration.testCaseGeneration.testCaseGenerator import generate_test_cases


def build_signal_test_collection(variables: Variables,
                                 signals_conditions: list[ExceptionExpression]) \
        -> list[SignalTestCollection]:
    test_collections = []

    for signal in signals_conditions:
        jml_problem = build_jml_problem(variables, [signal.expression])
        test_cases = generate_test_cases(jml_problem)
        test_collections.append(SignalTestCollection(test_cases, signal.exception_type))

    return test_collections
