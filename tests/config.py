import pathlib

TRANSLATOR_BASE_DIR = pathlib.Path(__file__).parent.parent / "translator"

TRANSLATOR_MAIN_PATH = TRANSLATOR_BASE_DIR / "src" / "main.py"

TRANSLATOR_PYTHON_EXECUTABLE_PATH = TRANSLATOR_BASE_DIR / ".venv" / "bin" / "python"

BUILD_PATH = pathlib.Path(__file__).parent / "build"

CASES_PATH = pathlib.Path(__file__).parent / "cases"

COMPILE_SCRIPT_PATH = pathlib.Path(__file__).parent / "compile.sh"
