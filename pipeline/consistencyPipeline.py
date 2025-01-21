import concurrent.futures

from codetiming import Timer

from codeExecution.compilation.javaCompilationRunner import compile_java_files
from codeExecution.vm.javaVm import start_java_vm, stop_java_vm
from definitions.consistencyTestCase import ConsistencyTestCase
from helper.logs.loggingHelper import log_info
from pipeline.consistencyResultGetter import ConsistencyResultGetter

inconsistency_pipeline_timer = Timer(name="run_consistency_pipeline", logger=None)


@inconsistency_pipeline_timer
def run_consistency_pipeline(consistency_tests: list[ConsistencyTestCase]):
    log_info("Starting consistency pipeline")

    try:
        # TODO: Start java vm and compile java files in parallel
        # start_java_vm()

        # Run compilation
        compile_java_files([c.java_code.file_path for c in consistency_tests])

        ordered_consistency_tests = sorted(consistency_tests, key=lambda x: get_consistency_test_case_order(x),
                                           reverse=True)

        results = []

        with concurrent.futures.ProcessPoolExecutor() as executor:
            for result in executor.map(task, ordered_consistency_tests):
                results.append(result)

        return results

    except Exception as e:
        raise e
    finally:
        stop_java_vm()


def get_consistency_test_case_order(consistency_test: ConsistencyTestCase):
    count = 0
    for param in consistency_test.method_info.parameters:
        if '[]' in param.name:  # Assuming array parameters are represented as lists
            count += 5
        else:
            count += 1
    return count


def task(value):
    start_java_vm()
    result = ConsistencyResultGetter().get_result(value)
    return result
