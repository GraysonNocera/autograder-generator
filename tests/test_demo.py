from gradergen.generator import Generator
import pathlib
import zipfile
import os

def test_demo():
    assert True

def test_writing_template_file():
    path_to_config = pathlib.Path(__file__).parents[1] / "examples" / "hw18.toml"
    generator = Generator(path_to_config)

    config = {}
    generator._generate_template_file(config, "test_files", "tests/test_files.py")
    generator.zip.close()

    with zipfile.ZipFile(f"{generator.config['executable']}.zip", "r") as zip:
        assert zip.namelist() == ["tests/test_files.py"]

    os.remove(f"{generator.config['executable']}.zip")