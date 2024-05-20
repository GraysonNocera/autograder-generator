import argparse
import tomllib
import zipfile
import pathlib
import os

class Generator:
    def __init__(self, path_to_config):
        self.path_to_config = path_to_config
        self.config = tomllib.load(open(path_to_config, "rb"))
        self.zip = zipfile.ZipFile(f"{self.config["executable"]}.zip", "w")

    def generate(self):
        path_to_inputs = self.config["tests"].get("input_directory", "inputs")
        path_to_expected = self.config["tests"].get("expected_directory", "expected")

        for file in os.listdir(path_to_inputs):
            self.zip.write(pathlib.Path(path_to_inputs) / pathlib.Path(file), pathlib.Path(path_to_inputs.split("/")[-1] / pathlib.Path(file)))

        for file in os.listdir(path_to_expected):
            self.zip.write(pathlib.Path(path_to_expected) / pathlib.Path(file), pathlib.Path(path_to_expected.split("/")[-1] / pathlib.Path(file)))

        self._generate_template_file(self.config, "setup-sh", "setup.sh")
        self._generate_template_file(self.config, "requirements-txt", "requirements.txt")
        self._generate_template_file(self.config, "run_tests-py", "run_tests.py")

        def inject(file):
            with open(file, "w") as f:
                f.write("#!/usr/bin/env bash\n")
                for file in self.config["files_from_student"]:
                    f.write(f"cp /autograder/submission/{file} /autograder/source/{file}\n")
                f.write("cd /autograder/source\n")
                f.write("python3.11 run_tests.py\n")
        self._generate_template_file(self.config, "run_autograder", "run_autograder", inject)
        self._generate_tests()

        path_to_weights = pathlib.Path(__file__).parent / "templates" / "tests" / "weights.py"
        self.zip.write(path_to_weights, "tests/weights.py")

        path_to_config_parser = pathlib.Path(__file__).parent / "templates" / "tests" / "config.py" 
        self.zip.write(path_to_config_parser, "tests/config.py")

        self.zip.write(self.path_to_config, pathlib.Path("tests") / self.path_to_config.split("/")[-1])

        self.zip.close()

    def _generate_tests(self):
        config = self.config["tests"]
        self._generate_template_file(config, "test_files", "tests/test_files.py")
        self._generate_template_file(config, "test_compile", "tests/test_compile.py")
        self._generate_template_file(config, "test_memory", "tests/test_memory.py")
        self._generate_template_file(config, "test_program", "tests/test_program.py")

    def _generate_template_file(self, base_config, key, default_filename, inject=None):
        config = base_config.get(key, {})
        if config.get("inject", False):
            self.zip.write(config["path"], default_filename)
            return
        path_to_template = pathlib.Path(__file__).parent / "templates" / default_filename
        if inject:
            inject(path_to_template)
        self.zip.write(path_to_template, default_filename)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Generate an autograder")
    parser.add_argument("config", help="Path to the configuration file")
    args = parser.parse_args()

    generator = Generator(args.config)
    generator.generate()