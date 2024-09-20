from definitions.ast.exceptionExpression import ExceptionExpression
from definitions.evaluations.tests.signalTestCollection import SignalTestCollection
from definitions.javaMethod import JavaMethod
from verification.jmlProblem.jmlProblemBuilder import JMLProblemBuilder
from verification.testCase.testCaseGenerator import TestCasesGenerator


class SignalTestCollectionBuilder:
    def __init__(self, jml_problem_builder=JMLProblemBuilder(), test_cases_generator=TestCasesGenerator()):
        self.jml_problem_builder = jml_problem_builder
        self.test_cases_generator = test_cases_generator

    def build(self, java_method: JavaMethod, signals_conditions: list[ExceptionExpression]) \
            -> list[SignalTestCollection]:
        test_collections = []

        for signal in signals_conditions:
            jml_problem = self.jml_problem_builder.build(java_method, [signal.expression])
            test_cases = self.test_cases_generator.generate(jml_problem)
            test_collections.append(SignalTestCollection(test_cases, signal.exception_type))

        return test_collections
