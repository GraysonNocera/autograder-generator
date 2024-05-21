import unittest
from gradescope_utils.autograder_utils.decorators import weight
from gradescope_utils.autograder_utils.files import check_submitted_files
import weights
from config import config
import pathlib

class TestFiles(unittest.TestCase):
    @weight(weights.TEST_FILES)
    def test_files(self):
        """Check submitted files"""
        missing_files = check_submitted_files(config["files_from_student"]) #, base=pathlib.Path(__file__).parents[1])
        for path in missing_files:
            print(f'Missing {path}')
        self.assertEqual(len(missing_files), 0, 'Missing required files')
        print('All required files submitted!')
