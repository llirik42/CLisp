# CLisp tests
Integration tests for CLisp. Performs the following pipeline: Scheme file => translate => compile => execute => comparing results.

## Prerequisites
Launch installing script:
```bash
./install.sh
```

Activate python environment:
```bash
source .venv/bin/activate
```

## Usage
```python main.py [-h] [-wd WITH_DIRECTORIES [WITH_DIRECTORIES ...]] [-wf WITH_FILES [WITH_FILES ...]] [-ed EXCLUDE_DIRECTORIES [EXCLUDE_DIRECTORIES ...]] [-ef EXCLUDE_FILES [EXCLUDE_FILES ...]] [-c]```

## Example
Run all tests ```python main.py```

Run tests only in the **const** directory ```python main.py -wd const```

Run all tests except those in the **logic** directory ```python main.py -ed logic```

Run all tests in the **arithmetic** directory excludes **div.test** ```python main.py -wd arithmetic -ef arithmetic/div.test```