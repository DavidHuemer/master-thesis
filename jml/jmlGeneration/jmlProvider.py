import os

from definitions.consistencyTestCase import ConsistencyTestCase
from jml.jmlGeneration.jmlStorage import get_stored_jml_for_test_case
from jml.jmlGeneration.jmlGenerator import JmlGenerator
from util.Singleton import Singleton


class JmlProvider(Singleton):
    def __init__(self, jml_generator: JmlGenerator = JmlGenerator()):
        self.jml_generator = jml_generator
        self.jml_file_path = os.getenv("JML_FILE")

    def reset(self):
        pass

    def get_jml(self, consistency_test: ConsistencyTestCase) -> str:
        if self.static_jml_exists():
            stored_jml = get_stored_jml_for_test_case(self.jml_file_path, consistency_test)
            if stored_jml is not None:
                return stored_jml

        return self.jml_generator.get_from_test_case(test_case=consistency_test)

    def static_jml_exists(self):
        return self.jml_file_path is not None

    def static_jml_exists_for_test_case(self, test_case: ConsistencyTestCase):
        return self.static_jml_exists() and get_stored_jml_for_test_case(self.jml_file_path, test_case) is not None
