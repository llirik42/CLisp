import argparse
import os
import subprocess
import sys
from pathlib import Path

parser = argparse.ArgumentParser(description= 'CLisp — Lisp-interpreter written on C.'
                                              ' This script reads a file containing code similar to Scheme (R5RS),'
                                              ' interprets it into the C language, compiles it into an executable file, and runs it.')
parser.add_argument('file', help='Path to .scm file')

args = parser.parse_args()

RED = '\033[0;31m'
NC = '\033[0m'

def print_error(message):
    print(f"{RED}{message}{NC}")


def main():
    input_path = Path(args.file).absolute()
    if not input_path.exists():
        print_error(f"Error: file {input_path} doesn't exist!")
        sys.exit(1)

    script_dir = Path(__file__).parent.absolute()
    os.chdir(script_dir)

    build_dir = script_dir / "build"
    build_dir.mkdir(exist_ok=True)

    out_file = build_dir / "out"
    if out_file.exists():
        out_file.unlink()

    lib_dir = script_dir / "lib"
    runtime_lib = lib_dir / "libruntime.so"

    if not lib_dir.exists() or not runtime_lib.exists():
        print_error("Error: no runtime library!")
        print_error("Execute ./install.sh")
        sys.exit(1)

    translator_venv = script_dir / "translator" / ".venv"
    if not translator_venv.exists():
        print_error("Error: no translator venv!")
        print_error("Execute ./install.sh")
        sys.exit(1)

    translator_dir = script_dir / "translator"
    out_c_file = build_dir / "out.c"

    translator_cmd = [
        translator_venv / "bin" / "python3",
        "-m", "src.main",
        "-f", str(input_path),
        "-o", str(out_c_file)
    ]

    try:
        subprocess.run(translator_cmd, check=True, cwd=translator_dir)
    except subprocess.CalledProcessError:
        print_error(f"Error during translation!")
        sys.exit(1)

    os.chdir(build_dir)

    compile_cmd = [
        "gcc",
        "-o", "out",
        "out.c",
        "-I../runtime",
        "-L../lib",
        "-lruntime",
        "-Wl,-rpath,../lib"
    ]

    try:
        subprocess.run(compile_cmd, check=True)
    except subprocess.CalledProcessError:
        print_error(f"Error during compilation!")
        sys.exit(1)

    try:
        subprocess.run(["./out"], check=True)
    except subprocess.CalledProcessError:
        print_error(f"Error during execution!")
        sys.exit(1)

if __name__ == "__main__":
    main()
