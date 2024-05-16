import argparse
import tomllib
import zipfile
import pathlib

class Generator:
    def __init__(self, config):
        self.config = config
        self.zip = zipfile.ZipFile(f"{self.config["global"]["executable"]}.zip", "w")

    def generate(self):        
        self._generate_template_file("setup-sh", "setup.sh")
        self._generate_template_file("requirements-txt", "requirements.txt")
        self._generate_template_file("run_tests-py", "run_tests.py")

        def inject(file):
            with open(file, "w") as f:
                f.write("#!/usr/bin/env bash\n")
                for file in self.config["global"]["files_from_student"]:
                    f.write(f"cp /autograder/submission/{file} /autograder/source/{file}\n")
                f.write("cd /autograder/source\n")
                f.write("python3 run_tests.py\n")
        self._generate_template_file("run_autograder", "run_autograder", inject)

        self.zip.close()

    def _generate_template_file(self, key, default_filename, inject=None):
        config = self.config[key] if key in self.config else {}
        if "injected" in config and config["injected"]:
            self.zip.write(config["path"], default_filename)
            return
        path_to_template = pathlib.Path(__file__).parent / "templates" / default_filename
        if inject:
            inject(path_to_template)
        self.zip.write(path_to_template, default_filename)
        return

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Generate an autograder")
    parser.add_argument("config", help="Path to the configuration file")
    args = parser.parse_args()

    with open(args.config, "rb") as f:
        config = tomllib.load(f)
        generator = Generator(config)
        generator.generate()