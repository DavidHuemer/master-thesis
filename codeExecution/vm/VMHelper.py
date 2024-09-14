import os

import jpype

from codeExecution.vm.jvmPathHelper import JvmPathHelper
from definitions import config
from helper.logs.loggingHelper import LoggingHelper


class VMHelper:
    """
    Helper class for the Java Virtual Machine (JVM).
    """

    def __init__(self, jvm=jpype, jvm_path_helper=JvmPathHelper()):
        self.jvm = jvm
        self.jvm_path_helper = jvm_path_helper

    def start(self):
        """
        Start the JVM.
        """

        dist_folder = os.path.join(os.getcwd(), config.CODE_DIST_FOLDER)
        jvm_path = self.jvm_path_helper.get_jvm_path()
        if not self.jvm.isJVMStarted():
            LoggingHelper.log_info(f"Starting JVM with path: {jvm_path}")
            self.jvm.startJVM(jvm_path, f"-Djava.class.path={dist_folder}")
        else:
            LoggingHelper.log_warning("JVM is already started")

    def close(self):
        """
        Close the JVM.
        """
        LoggingHelper.log_info("Closing JVM")
        if not self.jvm.isJVMStarted():
            LoggingHelper.log_warning("JVM is not started")
            return

        self.jvm.shutdownJVM()
