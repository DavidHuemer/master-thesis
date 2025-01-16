import sys

from dependency_injector.wiring import inject, Provide

from codeExecution.compilation.javaCompilationRunner import compile_java_files
from codeExecution.vm.javaVm import start_java_vm, stop_java_vm
from definitions.consistencyTestCase import ConsistencyTestCase
from helper.logs.loggingHelper import log_info
from pipeline.consistencyResultGetter import ConsistencyResultGetter
from pipeline.containers import PipelineContainer


@inject
def run_consistency_pipeline(consistency_tests: list[ConsistencyTestCase],
                             consistency_result_getter: ConsistencyResultGetter = Provide[
                                 PipelineContainer.consistency_result_getter]):
    log_info("Starting consistency pipeline")

    try:
        start_java_vm()

        # Run compilation
        compile_java_files([c.java_code.file_path for c in consistency_tests])

        size = sys.getsizeof(consistency_tests)

        return [consistency_result_getter.get_result(c) for c in consistency_tests]
    except Exception as e:
        raise e
    finally:
        stop_java_vm()
