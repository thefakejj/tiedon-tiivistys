Requirements: Poetry, Python 3.11 or newer

Install dependencies:

```bash
poetry install
```

In main.py, you can choose which text file to compress by editing the og_path variable. Note that the program only compresses ASCII-data correctly. The compressed data will be saved into binfile.bin located in the project's root directory. The program will print the compression ratio achieved using each algorithm as well as check that the decoded text matches the original.

To run the program, use

```bash
poetry run python3 src/main.py
```

To run tests, use

```bash
poetry run coverage run --branch -m pytest src
```

Create a coverage report either with

```bash
poetry run coverage report
```

```bash
poetry run coverage html
```
