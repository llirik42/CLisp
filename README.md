# CLisp — Lisp-interpreter written on C

## Prerequisites

Install [ANTLR4](https://github.com/antlr/antlr4/blob/master/doc/getting-started.md#installation).

Install uv:

```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```

Install libffi (example for Ubuntu)
```bash
sudo apt install libffi-dev
```

Launch installing script:

```bash
./install.sh
```

## Usage

```bash
python3 clisp.py input_file
```

## Example

```bash
python3 clisp.py example.scm
```
