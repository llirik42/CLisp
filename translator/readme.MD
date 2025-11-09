# CLisp translator

## Prerequisites

1. Install [ANTLR4](https://github.com/antlr/antlr4/blob/master/doc/getting-started.md#installation)
2. Generate python-code by ANTLR4

```bash
antlr4 -Dlanguage=Python3 -visitor Lisp.g4
```

> This should be done in activated python-environment with all dependencies installed

## Usage

```bash
python src/main.py [-h] [-o OUTPUT_FILE] [-p PROCEDURE_TABLE] [-t TEMPLATES] input_file
```
