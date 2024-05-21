# autograder-generator

ECE 264 utility for generating autograder files. Given a toml file like this:

```toml
files_from_student = [ "test.c", "test.h", "main.c" ] 
executable = "hwx" 

[tests] 

[tests.test_memory]
command_arguments = [ "inputs/input1.txt" ] 

[tests.test_program] 

[tests.test_program.input1] 
command_arguments = [ "inputs/input1.txt", 20 ] 
expected_output = "x yy 10" 

[tests.test_program.input2]
command_arguments = [ "inputs/input2.txt" ]
expected_output = "expected/expected1.txt"

[tests.test_program.input3]
command_arguments = [ 10, 20 ]
expected_output = "x yy 10"
```

# Usage

```bash
gradergen <path-to-toml-config>
```

Examples for the toml config can be found in the `examples` directory.

# Installation

```bash
pip install autograder
```