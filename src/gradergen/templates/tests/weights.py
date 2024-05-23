from config import config

DEFAULT_TEST_COMPILE = 10
DEFAULT_TEST_FILES = 10
DEFAULT_TEST_PROGRAM = 60
DEFAULT_TEST_MEMORY = 20

TEST_COMPILE = config["tests"].get("test_compile", {}).get("weight", DEFAULT_TEST_COMPILE)
TEST_FILES = config["tests"].get("test_files", {}).get("weight", DEFAULT_TEST_FILES)
TEST_PROGRAM = config["tests"]["test_program"].get("weight", DEFAULT_TEST_PROGRAM)
TEST_MEMORY = config["tests"]["test_memory"].get("weight", DEFAULT_TEST_MEMORY)

assert TEST_COMPILE + TEST_FILES + TEST_PROGRAM + TEST_MEMORY == 100, "Weights do not sum to 100"