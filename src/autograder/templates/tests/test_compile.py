import unittest
from gradescope_utils.autograder_utils.decorators import weight
import os
import weights
import subprocess
import test_files
from config import config

FILES = config.get("files_from_student", []) + config.get("files_from_solution", [])
EXEC = config.get("global", {}).get("executable", "a.out")
GCC = f"gcc -std=c11 -g -Wall -Wshadow --pedantic -Wvla -Werror"
COMMAND = f"{GCC} {FILES} -o {EXEC}"
COMMAND = config.get("tests", {}).get("test_compile", COMMAND)

class TestCompile(unittest.TestCase):

    @classmethod
    def setUpClass(self):
        test_files.TestFiles().test_files()

    @weight(weights.TEST_COMPILE)
    def test_compile(self):
        """Run compile command"""
        compiled = subprocess.run(COMMAND, shell=True, capture_output=True, cwd=os.path.dirname(os.path.dirname(__file__)))
        self.assertEqual(compiled.returncode, 0, f"Command {COMMAND} failed! {compiled.stderr, compiled.stdout}")
        print("Code compiles correctly!")