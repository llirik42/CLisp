# CLisp — Lisp-interpreter written on C

## Prerequisites

Install [ANTLR4](https://github.com/antlr/antlr4/blob/master/doc/getting-started.md#installation).

Install uv:

```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```

## Development

Compile runtime library:

```bash
./runtime_lib_complie.sh
```

## Usage

```bash
./clisp.sh input_file
```

## Example

```bash
./clisp.sh example.scm
```
