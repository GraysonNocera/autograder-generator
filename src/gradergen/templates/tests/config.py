import pathlib
import tomllib
import glob

def get_toml() -> str:
    toml_files = glob.glob("*.toml", root_dir=pathlib.Path(__file__).parent)
    if len(toml_files) == 0:
        raise FileNotFoundError("No .toml file found")
    if len(toml_files) > 1:
        raise FileNotFoundError("Multiple .toml files found")
    return toml_files[0]

path_to_toml = pathlib.Path(__file__).parent / get_toml()
config = None
with open(path_to_toml, 'rb') as f:
    config = tomllib.load(f)
    