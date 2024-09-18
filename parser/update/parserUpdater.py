import importlib
import os
import shutil

import parser
from definitions import config
from helper.processHelper import ProcessHelper
from parser import generated


class ParserUpdater:
    def __init__(self, process_helper=ProcessHelper()):
        self.process_helper = process_helper

    def update(self, path: str):
        self.process_helper.run_command(
            ["java", "-cp", config.ANTLR_JAR_PATH, config.ANTLR_COMMAND, "-Dlanguage=Python3", "-o", "parser/generated",
             path])

        cache_dir = os.path.join("parser/generated", "__pycache__")

        # Remove the cache
        if os.path.exists(cache_dir):
            shutil.rmtree(cache_dir)

        importlib.reload(parser.generated)
