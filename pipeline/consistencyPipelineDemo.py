from codeLoading.codeReader.javaCodeReader import JavaCodeReader
from helper.logs.loggingHelper import LoggingHelper
from pipeline.consistencyPipeline import ConsistencyPipeline
from testCases.consistencyTestCaseBuilder import ConsistencyTestCaseBuilder


def main():
    LoggingHelper.log_info("Starting consistency pipeline")

    pipeline = ConsistencyPipeline()
    pipeline.setup()

    code = JavaCodeReader().get_java_from_file("data\\code\\max\\Biggest.java")
    builder = ConsistencyTestCaseBuilder()
    test_cases = builder.build_test_cases([], [code])

    results = pipeline.get_results(test_cases)
    LoggingHelper.log_info(results[0])

    # Get Inconsistency test
    # class_info = ClassExtractionInfo("public", "Biggest", )
    # java_code = JavaCode("data\\code\\max\\Biggest.java", )
    #
    # inconsistency_test = InconsistencyTestCase()


if __name__ == "__main__":
    main()
