import sys


def read_from_file(input_file: str) -> str:
    with open(input_file) as f:
        return f.read()


def read_from_stdin() -> str:
    return sys.stdin.read()
