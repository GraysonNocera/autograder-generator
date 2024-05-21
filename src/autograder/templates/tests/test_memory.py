import unittest
from gradescope_utils.autograder_utils.decorators import weight
import pathlib
import test_compile
import test_files
import weights
import subprocess
from config import config

MEMORY_ERROR = 2
SEGMENTATION_FAULT = 139

class TestMemory(unittest.TestCase):
    
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

  @weight(weights.TEST_MEMORY)          
  def test_memory(self):
    executable = config["executable"]
    command_arguments = config["tests"]["test_memory"]["command_arguments"]
    command = f"valgrind -s --errors-for-leak-kinds=all --leak-check=full --show-leak-kinds=all --error-exitcode={MEMORY_ERROR} ./{executable} {' '.join(command_arguments)}"  
    
    result = subprocess.run(command, shell=True, capture_output=True, text=True, cwd=self._base_directory)
    print("VALGRIND OUTPUT:")
    print(result.stderr)
    
    self.assertNotEqual(result.returncode, MEMORY_ERROR, f"There are memory leaks in your program for valgrind command '{command}'!")
    self.assertNotEqual(result.returncode, SEGMENTATION_FAULT, f"Your program has a segmentation fault for valgrind command '{command}'!")
    print("No leaks or errors!") 
