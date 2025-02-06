import multiprocessing
import os

from codetiming import Timer

from codeExecution.compilation.javaCompilationRunner import compile_java_files
from codeExecution.vm.javaVm import is_java_vm_started, start_java_vm
from definitions.consistencyTestCase import ConsistencyTestCase
from helper.logs.loggingHelper import log_info
from jml.jmlFileHelper import get_jml_file
from pipeline.consistencyResultGetter import ConsistencyResultGetter
from util import multiProcessUtil
from util.envUtil import get_required_env_dict

inconsistency_pipeline_timer = Timer(name="run_consistency_pipeline", logger=None)


@inconsistency_pipeline_timer
def run_consistency_pipeline(consistency_tests: list[ConsistencyTestCase]):
    log_info("Starting consistency pipeline")
    compile_java_files([c.java_code.file_path for c in consistency_tests])
    env_dict = get_required_env_dict()

    log_lock = multiprocessing.Lock()
    ordered_consistency_tests = sorted(consistency_tests, key=lambda x: get_consistency_test_case_order(x),
                                       reverse=True)

    jml_file_path = get_jml_file()

    with multiprocessing.Pool(16, initializer=initialize_consistency_process,
                              initargs=(env_dict, log_lock, jml_file_path)) as pool:  # 4 Prozesse wiederverwenden
        results = pool.map(run_consistency_process, ordered_consistency_tests)

    return results

    # initialize_consistency_process(env_dict, log_lock, jml_file_path)
    # results = [run_consistency_process(v) for v in ordered_consistency_tests]

    # results = []
    # with futures.ProcessPoolExecutor(initializer=initialize_consistency_process,
    #                                  initargs=(env_dict, log_lock)) as executor:
    #     for result in executor.map(run_consistency_process, ordered_consistency_tests):
    #         results.append(result)
    #
    # return results

    # Run compilation
    # compile_java_files([c.java_code.file_path for c in consistency_tests])
    #
    # ordered_consistency_tests = sorted(consistency_tests, key=lambda x: get_consistency_test_case_order(x),
    #                                    reverse=True)
    #
    # results = []
    #
    # # crete dict of environment variables
    # env_dict = dict(os.environ)
    #
    # log_lock = multiprocessing.Lock()
    #
    # with concurrent.futures.ProcessPoolExecutor(initializer=initialize_consistency_process,
    #                                             initargs=(env_dict, log_lock)) as executor:
    #
    #     for result in executor.map(run_consistency_process, ordered_consistency_tests):
    #         results.append(result)
    #
    # return results


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

    os.environ["JML_FILES"] = jml_files_path


def run_consistency_process(value):
    # with LOCK:
    #     log_info(f"Running consistency process for {str(value)}")

    if not is_java_vm_started():
        start_java_vm()

    return ConsistencyResultGetter().get_result(value)
