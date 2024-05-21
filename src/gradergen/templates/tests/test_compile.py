import unittest
from gradescope_utils.autograder_utils.decorators import weight
import weights
import subprocess
import test_files
from config import config
import pathlib

FILES = config["files_from_student"] + config.get("files_from_solution", [])
EXEC = config["executable"]
GCC = f"gcc -std=c11 -g -Wall -Wshadow --pedantic -Wvla -Werror"
COMMAND = f"{GCC} {' '.join(FILES)} -o {EXEC}"
COMMAND = config["tests"].get("test_compile", {}).get("command", COMMAND)

class TestCompile(unittest.TestCase):

    @classmethod
    def setUpClass(self):
        test_files.TestFiles().test_files()

    @weight(weights.TEST_COMPILE)
    def test_compile(self):
        """Run compile command"""
        compiled = subprocess.run(COMMAND, shell=True, capture_output=True, cwd=pathlib.Path(__file__).parents[1])
        self.assertEqual(compiled.returncode, 0, f"Command {COMMAND} failed! {compiled.stderr, compiled.stdout}")
        print("Code compiles correctly!")
