import argparse
import os
import subprocess
import pytest

from config import INSTALL_SCRIPT, BUILD_PATH, CASES_PATH
from utils import delete_all_files_in_dir, copy_directory_structure

parser = argparse.ArgumentParser(description='This is a set of integration tests for CLisp.'
                                             ' For each Scheme file in the ./cases/* directory, it performs the following pipeline:'
                                             'translates the Scheme code to C, compiles the C code into an '
                                             'executable, runs the executable, and compares its output to the '
                                             'expected result.')
parser.add_argument('-wd', '--with-directories', nargs='+', help='Apply tests only to files in specified directories relative ./cases')
parser.add_argument('-wf', '--with-files', nargs='+', help='Apply tests only to files relative ./cases.'
                                                           ' Merges with -wd.')
parser.add_argument('-ed', '--exclude-directories', nargs='+', help='Exclude all tests in specified directories relative ./cases')
parser.add_argument('-ef', '--exclude-files', nargs='+', help='Exclude tests only to files relative ./cases.'
                                                           ' Merges with -ed.')
parser.add_argument('-c', '--clear', action='store_true', default=False, help='Clear ./build directory after running tests.')

args = parser.parse_args()

if __name__ == '__main__':
    try:
        subprocess.run(
            [str(INSTALL_SCRIPT)],
            capture_output=True,
            check=True,
        )
    except subprocess.CalledProcessError as e:
        raise RuntimeError(
            f"Error during launching install script. Stderr:\n{e.stderr}"
        )

    tests_files_paths = []

    if args.with_directories:
        for directory_path in args.with_directories:
            path = CASES_PATH / directory_path
            for file_path in path.rglob("*.test"):
                tests_files_paths.append(str(file_path))

    if args.with_files:
        for file_path in args.with_files:
            path = CASES_PATH / file_path
            if not path.exists():
                raise FileNotFoundError(f'File not found: {str(path)}')
            tests_files_paths.append(str(path))

    if len(tests_files_paths) == 0:
        for file_path in CASES_PATH.rglob("*.test"):
            tests_files_paths.append(str(file_path))

    if args.exclude_directories:
        for directory_path in args.exclude_directories:
            path = CASES_PATH / directory_path
            for file_path in path.rglob("*.test"):
                try:
                    tests_files_paths.remove(str(path))
                except ValueError:
                    pass

    if args.exclude_files:
        for file_path in args.exclude_files:
            path = CASES_PATH / file_path
            try:
                tests_files_paths.remove(str(path))
            except ValueError:
                pass


    if len(tests_files_paths) == 0:
        raise ValueError('No test files found!')

    os.environ['TEST_FILES'] = os.pathsep.join(tests_files_paths)
    copy_directory_structure(CASES_PATH, BUILD_PATH)
    delete_all_files_in_dir(BUILD_PATH)

    pytest.main(["test.py::test_with_path_env", "-v", "-s"])

    if args.clear:
        delete_all_files_in_dir(BUILD_PATH)

