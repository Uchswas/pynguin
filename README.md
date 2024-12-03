# Pynguin Test Case Generator

This repository demonstrates the usage of the modified Pynguin module to automatically generate unit tests for Python functions, with a focus on Pandas-based operations. 

## Table of Contents
- [Getting Started](#getting-started)
- [Directory Structure](#directory-structure)
- [Usage](#usage)
- [Output](#output)

---

## Getting Started
1. Clone this repository and navigate to its root directory.
```bash
  git clone https://github.com/Uchswas/pynguin.git
  cd pynguin
  git checkout dataframe_final
```
2. Create a virtual environment.
```bash
  python -m venv venv_dataframe
  source venv_dataframe/bin/activate
```
3. Install the updated Pynguin module.
```bash
  pip install .
```
4. Verify that the correct Pynguin module is installed.
```bash
  which pynguin
```
  This should return the path of the local directory where the Pynguin source code resides.


## Directory Structure
```
repo/
├── ourtask/
│   ├── run.py               # Script to run Pynguin
│   ├── numpy_example.py        # Contains basic Pandas-based functions
├── generated_tests/            # Folder containing auto-generated test files
├── reports/
│   ├── statistics.csv          # File containing code coverage statistics
```

## Usage
1. Navigate to the ourtask directory
```bash
cd ourtask
```
2. Run the python.py script to generate test cases
```bash
python run.py
```
This will:
- Execute the modified Pynguin module.
- Create test files for the functions in numpy_example.py.

## Output

1. Generated Test Files:
Test files will be stored in the generated_tests/ directory. These files contain unit tests for the functions in numpy_example.py.

2. Code Coverage Report
Code coverage statistics for the generated tests are stored in the reports/statistics.csv file. This file provides metrics on how much of your code is covered by the auto-generated tests.
