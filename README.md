# Xvert_docstring_plain2np

## Description

Xvert_docstring_plain2np is a command line tool to convert the doctrings of a code base form plain format to
NumPy format.
    

## Installation

```
git clone https://github.com/FranckLejzerowicz/Xvert_docstring_plain2np.git
cd Xvert_docstring_plain2np
pip install -e .
```

```
pip install --upgrade git+https://github.com/FranckLejzerowicz/Xvert_docstring_plain2np.git
```

*_Note that pip should be for python3_

## Input

A path to a folder containing the package files within which there's docstrings to convert (option `-i`).
 
## Outputs

All the files with converted docstrings are copied with a `.Xcvrted` extension.
Check these files before applying the suggested move command.

#### Input / Output example

blah.


## Usage

```
Usage: Xvert_docstring_plain2np [OPTIONS]

Options:
  -i, --i-folder TEXT  Folder to walk through to find files for conversion.
                       [required]
  -o, --o-mv TEXT      File path to the script to run to replace the non-
                       converted files with the converted files (after
                       checking).
  --version            Show the version and exit.
  --help               Show this message and exit.

```

## Usage example

Running: 
```
Xvert_docstring_plain2np -i ./Xvert_docstring_plain2np/tests/code_base -o ./Xvert_docstring_plain2np/tests/code_base.sh 
```

On these files:
```
└─ code_base
    ├── _a_test.py
    ├── _b_test.py
    └── _c_test.py
```


Would create these files:
```
├── code_base
│   ├── _a_test.py_xverted.py
│   ├── _b_test.py_xverted.py
│   └── _c_test.py_xverted.py
└── code_base.sh
```

Including the `_xverted.py` copies with NumPy docstrings, and the `code_base.sh` script suggesting move commands:
```
mv ./Xvert_docstring_plain2np/tests/code_base/_a_test.py_xverted.py ./Xvert_docstring_plain2np/tests/code_base/_a_test.py
mv ./Xvert_docstring_plain2np/tests/code_base/_b_test.py_xverted.py ./Xvert_docstring_plain2np/tests/code_base/_b_test.py
mv ./Xvert_docstring_plain2np/tests/code_base/_c_test.py_xverted.py ./Xvert_docstring_plain2np/tests/code_base/_c_test.py
```

### Bug Reports

contact `flejzerowicz@health.ucsd.edu`