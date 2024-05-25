import unittest
from gradescope_utils.autograder_utils.decorators import weight
import test_compile
import test_files
import weights
import subprocess
from config import config
from parameterized import parameterized
import pathlib
from typing import List

NUM_TEST_PROGRAM = sum(1 for value in config["tests"]["test_program"].values() if isinstance(value, dict)) 
NUM_TESTS_MEMORY = sum(1 for value in config["tests"]["test_memory"].values() if isinstance(value, dict))
MEMORY_ERROR = 2
SEGMENTATION_FAULT = 139

def load_program_test_cases() -> List[tuple[str, List[str], str, str]]:
    test_cases = []
    config_tests = config["tests"]["test_program"]
    for key in config_tests:
        if isinstance(config_tests[key], dict):
            command_arguments = config_tests[key]["command_arguments"]
            expected_output = config_tests[key]["expected_output"]
            output = config_tests[key].get("output", "stdout")

            test_cases.append((key, command_arguments, output, expected_output))

    return test_cases

def load_memory_test_cases() -> List[tuple[str, List[str]]]:
    test_cases = []
    config_tests = config["tests"]["test_memory"]
    for key in config_tests:
        if isinstance(config_tests[key], dict):
            command_arguments = config_tests[key]["command_arguments"]
            test_cases.append((key, command_arguments))

    return test_cases

class TestProgram(unittest.TestCase):
    @classmethod
    def setUpClass(self):
        
        test_files.TestFiles().test_files()
        test_compile.TestCompile().test_compile()

        self._base_directory = pathlib.Path(__file__).parents[1]

        input_directory_name = config["tests"].get("input_directory", "inputs")
        self._input_directory = self._base_directory / input_directory_name 
        self._input_files = self._input_directory.glob("*")

        expected_directory_name = config["tests"].get("expected_directory", "expected")
        self._expected_directory = self._base_directory / expected_directory_name
        self._expected_files = self._expected_directory.glob("*")

    @parameterized.expand(load_memory_test_cases)
    @weight(weights.TEST_MEMORY / NUM_TESTS_MEMORY)
    def test_memory(self, _, command_arguments: List[str]):
        executable = config["executable"]
        command = f"valgrind -s --errors-for-leak-kinds=all --leak-check=full --show-leak-kinds=all --error-exitcode={MEMORY_ERROR} ./{executable} {' '.join(command_arguments)}"  
        
        result = subprocess.run(command, shell=True, capture_output=True, text=True, cwd=self._base_directory)
        print("VALGRIND OUTPUT:")
        print(result.stderr)
        
        self.assertNotEqual(result.returncode, MEMORY_ERROR, f"There are memory leaks in your program for valgrind command '{command}'!")
        self.assertNotEqual(result.returncode, SEGMENTATION_FAULT, f"Your program has a segmentation fault for valgrind command '{command}'!")
        print("No leaks or errors!") 

    @parameterized.expand(load_program_test_cases)
    @weight(weights.TEST_PROGRAM / NUM_TEST_PROGRAM)
    def test_program(self, _, command_arguments: List[str], output: str, expected_output: str):
        executable = config["executable"]
        command = f"./{executable} {' '.join(command_arguments)}"
        process = subprocess.run(command, shell=True, capture_output=True, text=True, cwd=pathlib.Path(__file__).parents[1])

        if output == "stdout":
            result = process.stdout
        else:
            with open(output, "r") as f:
                result = f.read()
        
        if isinstance(expected_output, dict) and expected_output.get("literal", ""):
            expected = expected_output
        else:
            with open(expected_output, "r") as f:
                expected = f.read()

        if result != expected:
            self.print_difference(result, expected)
            self.assertTrue(False)

        self.assertTrue(True)
    
    def print_difference(self, result: str, expected: str) -> None: 
        result_split = set(result.split("\n"))
        expected_split = set(expected.split("\n"))
        missing_from_output = expected_split.difference(result_split)
        missing_from_output = "\n".join(missing_from_output)
        extra_from_output = result_split.difference(expected_split)
        extra_from_output = "\n".join(extra_from_output)
        print("RESULTS\n")
        print("Lines missing from your output (NOT NECESSARILY IN THIS ORDER):")
        print("-----START-----")
        print(missing_from_output)
        print("----- END -----\n")
        print("Extra lines from your output (NOT NECESSARILY IN THIS ORDER):")
        print("-----START-----")
        print(extra_from_output)
        print("----- END -----")