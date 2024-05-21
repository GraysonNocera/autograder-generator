import argparse
from gradergen.generator import Generator

def main():
    parser = argparse.ArgumentParser(description="Generate an autograder")
    parser.add_argument("config", help="Path to the configuration file")
    args = parser.parse_args()

    generator = Generator(args.config)
    generator.generate()

if __name__ == "__main__":
    main()