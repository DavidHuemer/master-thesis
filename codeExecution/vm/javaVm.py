import os

import jpype

from codeExecution.vm.javaPaths import get_jvm_path
from definitions import config
from helper.logs.loggingHelper import log_info, log_warning


def start_java_vm():
    dist_folder = os.path.join(os.getcwd(), config.CODE_DIST_FOLDER)
    jvm_path = get_jvm_path()
    if not jpype.isJVMStarted():
        log_info(f"Starting JVM with path: {jvm_path}")
        jpype.startJVM(jvm_path, f"-Djava.class.path={dist_folder}")
    else:
        log_warning("JVM is already started")


def is_java_vm_started():
    return jpype.isJVMStarted()


def stop_java_vm():
    log_info("Closing JVM")
    if not jpype.isJVMStarted():
        log_warning("JVM is not started")
        return

    jpype.shutdownJVM()
