from codeExecution.vm.VMHelper import VMHelper
from codeLoading.codeReader.javaCodeReader import JavaCodeReader
from helper.logs.loggingHelper import LoggingHelper
from pipeline.jmlVerifier.jmlVerifier import JmlVerifier
from testCases.consistencyTestCaseBuilder import ConsistencyTestCaseBuilder

jml_code = ("//@ requires arr != null;\n"
            "//@ ensures (\\forall int i, j; 0 <= i && i < j && j < arr.length; arr[i] != arr[j]);")


def main():
    vm_helper = VMHelper()
    try:
        vm_helper.start()

        code = JavaCodeReader().get_java_from_file("data\\code\\comparison\\DistinctArray.java")
        builder = ConsistencyTestCaseBuilder()
        test_cases = builder.build_test_cases([], [code])

        jml_verifier = JmlVerifier()
        jml_verifier.setup()
        result = jml_verifier.verify(test_cases[0], jml_code)

        if result.consistent is None:
            LoggingHelper.log_error(result)
        else:
            LoggingHelper.log_info(result)
    except Exception as e:
        raise e
    finally:
        vm_helper.close()


if __name__ == "__main__":
    main()
