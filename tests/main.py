import subprocess
from pathlib import Path
import pytest

@pytest.fixture(scope="session")
def run_translator():

    base_dir = Path(__file__).parent.parent / "translator"
    main_script = base_dir / "src" / "main.py"

    venv_path = base_dir / ".venv"
    python_executable = venv_path / "bin" / "python"

    def _run_translator(args="", input_text="", cwd=None):
        """
        Launching translator with args.

        Args:
            args: command line args string.
            input_text: text for stdin.
            cwd: current working directory of translator script.
        """

        if cwd is None:
            cwd = base_dir

        command = [str(python_executable), str(main_script)] + args.split()

        result = subprocess.run(
            command,
            capture_output=True,
            text=True,
            input=input_text,
            cwd=cwd
        )

        return result

    return _run_translator

def test_main(run_translator):
    run_translator('../example.scm -o ../tests/build/out.c')
