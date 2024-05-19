from config import config

TEST_COMPILE = config["tests"].get("test_compile", {}).get("weight",10)
TEST_FILES = config["tests"].get("test_files", {}).get("weight", 10)
TEST_PROGRAM = config["tests"]["test_program"].get("weight", 60)
TEST_MEMORY = config["tests"]["test_memory"].get("weight", 20)

assert TEST_COMPILE + TEST_FILES + TEST_PROGRAM + TEST_MEMORY == 100, "Weights do not sum to 100"