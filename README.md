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
 

## Example
 

## Usage

```
Usage: Xvert_docstring_plain2np [OPTIONS]

Options:
  -i, --i-folder TEXT   Folder to walk through to find files for export.
                        [required]
  --version             Show the version and exit.
  --help                Show this message and exit.
```

### Bug Reports

contact `flejzerowicz@health.ucsd.edu`