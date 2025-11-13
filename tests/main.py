import os
import subprocess
from pathlib import Path
from subprocess import CompletedProcess

import pytest

from config import (TRANSLATOR_PATH, TRANSLATOR_BASE_DIR, TRANSLATOR_PYTHON_EXECUTABLE_PATH,
                    CASES_PATH, BUILD_PATH, COMPILE_SCRIPT_PATH)


@pytest.fixture(scope="session")
def run_translator():

    def _run_translator(args="", input_text="", cwd=None):
        """
        Launching translator with args.

        Args:
            args: command line args string.
            input_text: text for stdin.
            cwd: current working directory of translator script.
        """

        if cwd is None:
            cwd = TRANSLATOR_BASE_DIR

        command = [str(TRANSLATOR_PYTHON_EXECUTABLE_PATH), "-m",  TRANSLATOR_PATH] + args.split()
        _env = os.environ
        _env["PYTHONPATH"] = str(TRANSLATOR_BASE_DIR)

        result = subprocess.run(
            command,
            capture_output=True,
            text=True,
            input=input_text,
            cwd=cwd,
            check=True,
            env=_env
        )

        return result

    return _run_translator


def copy_directory_structure(source_dir, target_dir):
    source_path = Path(source_dir)
    target_path = Path(target_dir)

    target_path.mkdir(exist_ok=True)

    for dir_path in source_path.rglob('*'):
        if dir_path.is_dir():
            relative_path = dir_path.relative_to(source_path)
            new_dir = target_path / relative_path
            new_dir.mkdir(exist_ok=True)


def test_all_cases(run_translator):
    copy_directory_structure(CASES_PATH, BUILD_PATH)
    for file_path in CASES_PATH.rglob('*.txt'):
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                lines = [line.strip() for line in f.readlines()]
        except Exception as e:
            print(f"File reading error {file_path}: {e}")


        if lines[0] != '******************[TESTING CODE]******************':
            raise ValueError(f'Case: {file_path} wrong file format: no testing code block.')
        curr_line = 1
        program_code = ''
        while lines[curr_line] != '******************[EXPECTED OUT]******************':
            if curr_line == len(lines):
                raise ValueError(f'Case: {file_path} wrong file format: no expecting out block.')
            program_code += (lines[curr_line] + '\n')
            curr_line += 1

        file_path_raw = file_path.relative_to(CASES_PATH)

        try:
            run_translator(f'-i -o ../tests/build/{file_path_raw}.c', input_text=program_code)
        except subprocess.CalledProcessError as e:
            raise RuntimeError(
                f'Case: {file_path} error during executing translator. Stderr:\n{e.stderr}')

        try:
            subprocess.run([str(COMPILE_SCRIPT_PATH), f"{file_path_raw}.c"], capture_output=True, check=True)
        except subprocess.CalledProcessError as e:
            raise RuntimeError(
                f'Case: {file_path} error during compiling c program. Stderr:\n{e.stderr}')

        program_result: CompletedProcess[str] = subprocess.run([f'{str(BUILD_PATH)}/{file_path_raw}.out'],
                                capture_output=True,
                                text=True)

        if program_result.returncode:
            raise RuntimeError(f'Case: {file_path} Error during execution program. Stderr:\n{program_result.stderr}.')

        out_lines = program_result.stdout.splitlines()

        curr_line += 1
        out_lines_pos = 0

        if len(out_lines) != (len(lines) - curr_line):
            raise RuntimeError(f'Case: {file_path} count of program output lines is not equal to the expected line count in case file.'
                               f' Expected {len(out_lines)}. Got {len(lines) - curr_line}.')

        while curr_line < len(lines):
            assert lines[curr_line].strip() == out_lines[out_lines_pos], (f"Case: {file_path} output line: {out_lines_pos + 1}. "
                                                                          f"Expected {lines[curr_line]}. Got {out_lines[out_lines_pos]}")
            out_lines_pos += 1
            curr_line += 1
