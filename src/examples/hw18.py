import tomllib
import pathlib

with open('hw18.toml', 'rb') as f:
    data = tomllib.load(f)
    print(data)
