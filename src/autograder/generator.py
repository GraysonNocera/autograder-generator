import argparse
import tomllib
import zipfile
import pathlib

class Generator:
    def __init__(self, config):
        self.config = config
        self.zip = zipfile.ZipFile(f"{self.config["global"]["executable"]}.zip", "w")

    def generate(self):        
        self._generate_template_file(self.config, "setup-sh", "setup.sh")
        self._generate_template_file(self.config, "requirements-txt", "requirements.txt")
        self._generate_template_file(self.config, "run_tests-py", "run_tests.py")

        def inject(file):
            with open(file, "w") as f:
                f.write("#!/usr/bin/env bash\n")
                for file in self.config["global"]["files_from_student"]:
                    f.write(f"cp /autograder/submission/{file} /autograder/source/{file}\n")
                f.write("cd /autograder/source\n")
                f.write("python3 run_tests.py\n")
        self._generate_template_file(self.config, "run_autograder", "run_autograder", inject)
        self._generate_tests()

        self.zip.close()

    def _generate_tests(self):
        config = self.config.get("tests")
        self._generate_template_file(config, "test_files", "tests/test_files.py")
        self._generate_template_file(config, "test_gcc", "tests/test_gcc.py")
        self._generate_template_file(config, "test_memory", "tests/test_memory.py")
        self._generate_template_file(config, "test_compile", "tests/test_compile.py")

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

    with open(args.config, "rb") as f:
        config = tomllib.load(f)
        generator = Generator(config)
        generator.generate()