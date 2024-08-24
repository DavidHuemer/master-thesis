from unittest import TestCase

import pytest

from codeLoading.codeReader.javaClassReader import JavaClassReader


def get_java_example(number):
    with open(f"testdata/javaClassTestData/test-{number}.txt", "r") as file:
        file_content = file.read()
        # get first line of the file
        file_lines = file_content.split("\n")
        meta = file_lines[0]
        meta_parts = meta.split(";")

        # Find index of line that contains ===
        example_split_line = file_lines.index("===")

        # Expected content is everything after the first line and before the === line
        expected_content = "\n".join(file_lines[1:example_split_line]).strip()

        # The example is everything after the === line
        example = "\n".join(file_lines[example_split_line + 1:])

        return meta_parts[0], meta_parts[1], expected_content, example


class TestJavaClassReader(TestCase):

    def test_add(self):
        test_data = list(range(1, 4))
        for idx in test_data:
            with self.subTest(idx=idx, msg=f"Test {idx}"):
                self.run_test(idx)

    def run_test(self, number):
        protection, name, content, example = get_java_example(number)
        result = JavaClassReader.get_java_class_from_code(example)
        self.assertEqual(protection, result.class_protection)
        self.assertEqual(name, result.class_name)
        self.assertEqual(content, result.code)
