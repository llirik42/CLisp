# CLisp tests
Integration tests for CLisp. Performs the following pipeline: Scheme file => translate => compile => execute => comparing results.

## Prerequisites
Launch installing script:
```bash
./install.sh
```

## Usage
```./run.sh [-h] [-wd WITH_DIRECTORIES [WITH_DIRECTORIES ...]] [-wf WITH_FILES [WITH_FILES ...]] [-ed EXCLUDE_DIRECTORIES [EXCLUDE_DIRECTORIES ...]] [-ef EXCLUDE_FILES [EXCLUDE_FILES ...]] [-c]```

**Examples**:

* Run all tests ```./run.sh```

* Run tests only in the **const** directory ```./run.sh -wd const```

* Run all tests except those in the **logic** directory ```./run.sh -ed logic```

* Run all tests in the **arithmetic** directory excludes **div.test** ```./run.sh -wd arithmetic -ef arithmetic/div.test```

## Memory tests

Memory tests use valgrind that uses generated files of all test cases.

**Usage**:

```bash
./memory.sh
```
