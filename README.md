# CLisp — Lisp interpreter written on C

* [Documentation](doc.md)

## Prerequisites

1. Install [ANTLR4](https://github.com/antlr/antlr4/blob/master/doc/getting-started.md#installation).

2. Install uv:

```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```

3. Install libffi (example for Ubuntu)

```bash
sudo apt install libffi-dev
```

4. Launch installing script:

```bash
./install.sh
```

## Usage

```bash
python3 clisp.py input_file
```

**Example**

```bash
python3 clisp.py example.scm
```

```
6
```
