# tests.py

import unittest
from functions.get_files_info import get_files_info

def pretty_print(s):
    print(f"\n{s}")

class TestGetFilesInfo(unittest.TestCase):
    def test_get_files_info_current_dir(self):
        expected = """Result for current directory:
 - main.py: file_size=729 bytes, is_dir=False
 - pkg: file_size=4096 bytes, is_dir=True
 - tests.py: file_size=1342 bytes, is_dir=False
"""
        result = get_files_info("calculator", ".")
        pretty_print(result)
        self.assertEqual(expected, result)

    def test_get_files_info_pkg_dir(self):
        expected = """Result for 'pkg' directory:
 - calculator.py: file_size=1737 bytes, is_dir=False
 - render.py: file_size=388 bytes, is_dir=False
"""
        result = get_files_info("calculator", "pkg")
        pretty_print(result)
        self.assertEqual(expected, result)

    def test_get_files_info_slashbin_dir(self):
        expected = """Result for '/bin' directory:
Error: Cannot list "/bin" as it is outside the permitted working directory"""
        result = get_files_info("calculator", "/bin")
        pretty_print(result)
        self.assertEqual(expected, result)

    def test_get_files_info_dotdotslash_dir(self):
        expected = """Result for '../' directory:
Error: Cannot list "../" as it is outside the permitted working directory"""
        result = get_files_info("calculator", "../")
        pretty_print(result)
        self.assertEqual(expected, result)


if __name__ == "__main__":
    unittest.main()