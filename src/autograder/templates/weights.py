from config import config

TEST_COMPILE = config.get("tests", {}).get("test_compile", 10)
TEST_FILES = config.get("tests", {}).get("test_files", 10)
TEST_PROGRAM = config.get("tests", {}).get("test_program", 60)
TEST_MEMORY = config.get("tests", {}).get("test_memory", 20)

assert TEST_COMPILE + TEST_FILES + TEST_PROGRAM + TEST_MEMORY == 100, "Weights do not sum to 100"