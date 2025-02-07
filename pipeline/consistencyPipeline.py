import concurrent
import multiprocessing
import os
from concurrent import futures

from codetiming import Timer

from codeExecution.compilation.javaCompilationRunner import compile_java_files
from codeExecution.vm.javaVm import is_java_vm_started, start_java_vm
from definitions.consistencyTestCase import ConsistencyTestCase
from definitions.envKeys import JML_FILE
from helper.logs.loggingHelper import log_info, log_error
from jml.jmlFileHelper import get_jml_file
from pipeline.consistencyResultGetter import ConsistencyResultGetter
from util import multiProcessUtil
from util.envUtil import get_required_env_dict
from verification.result.verificationResultFactory import VerificationResultFactory

inconsistency_pipeline_timer = Timer(name="run_consistency_pipeline", logger=None)


@inconsistency_pipeline_timer
def run_consistency_pipeline(consistency_tests: list[ConsistencyTestCase]):
    log_info("Starting consistency pipeline")

    try:
        compile_java_files([c.java_code.file_path for c in consistency_tests])

        parallel = os.getenv("PARALLEL") == "true"
        if parallel:
            return run_consistency_pipeline_parallel(consistency_tests)

        else:
            return run_consistency_pipeline_sequential(consistency_tests)
    except Exception as e:
        log_error(f"An error occurred when running the consistency pipeline {str(e)}")
        return [VerificationResultFactory.by_exception(test_case, e) for test_case in consistency_tests]


def run_consistency_pipeline_parallel(consistency_tests: list[ConsistencyTestCase]):
    env_dict = get_required_env_dict()
    log_lock = multiprocessing.Lock()
    ordered_consistency_tests = sorted(consistency_tests, key=lambda x: get_consistency_test_case_order(x),
                                       reverse=True)

    results = []
    with concurrent.futures.ProcessPoolExecutor(initializer=initialize_consistency_process,
                                                initargs=(env_dict, log_lock, get_jml_file())) as executor:
        for result in executor.map(run_consistency_process, ordered_consistency_tests):
            results.append(result)

    return results


def run_consistency_pipeline_sequential(consistency_tests: list[ConsistencyTestCase]):
    return [run_consistency_process(test_case) for test_case in consistency_tests]


def get_consistency_test_case_order(consistency_test: ConsistencyTestCase):
    count = 0
    for param in consistency_test.method_info.parameters:
        if param.is_array():  # Assuming array parameters are represented as lists
            count += 5
        else:
            count += 1
    return count


def initialize_consistency_process(env_dict: dict[str, str], log_lock: multiprocessing.Lock, jml_files_path: str):
    multiProcessUtil.lock = log_lock

    for key, value in env_dict.items():
        os.environ[key] = value

    os.environ[JML_FILE] = jml_files_path
    log_info("Initialized consistency process")


def run_consistency_process(value):
    try:
        log_info(f"Running consistency process for {str(value)}")

        if not is_java_vm_started():
            start_java_vm()

        return ConsistencyResultGetter().get_result(value)
    except Exception as e:
        return VerificationResultFactory.by_exception(value, e)
