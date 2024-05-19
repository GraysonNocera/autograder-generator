import unittest
from gradescope_utils.autograder_utils.decorators import weight
import os
import test_compile
import test_files
import weights
import subprocess
from config import config

MEMORY_ERROR = 2
SEGMENTATION_FAULT = -11
NUM_TESTS = 1

class TestMemory(unittest.TestCase):
    
  @classmethod
  def setUpClass(self):
      test_files.TestFiles().test_files()
      test_compile.TestCompile().test_compile()

      self._base_directory = os.path.dirname(os.path.dirname(__file__))

      input_directory_name = config["tests"].get("input_directory", "inputs")    
      self._input_directory = os.path.join(self._base_directory, input_directory_name)
      self._input_files = os.listdir(self._input_directory)

      expected_directory_name = config["tests"].get("expected_directory", "expected")
      self._expected_directory = os.path.join(self._base_directory, expected_directory_name)
      self._expected_files = os.listdir(self._expected_directory)

  @weight(weights.TEST_MEMORY)          
  def test_memory(self):
    executable = config["global"]["executable"]
    command_arguments = config["tests"]["test_memory"]["command_arguments"]
    command = f"valgrind -s --errors-for-leak-kinds=all --leak-check=full --show-leak-kinds=all --error-exitcode={MEMORY_ERROR} ./{executable} {' '.join(command_arguments)}"  
    
    result = subprocess.run(command, shell=True, capture_output=True, text=True, cwd=self._base_directory)
    print("VALGRIND OUTPUT:")
    print(result.stderr)
    
    self.assertFalse(result.returncode in {MEMORY_ERROR, SEGMENTATION_FAULT}, f"There are memory leaks in your program for valgrind command '{command}'!")
    print("No leaks or errors!") 
