This is a bit of a placeholder guide, but here's how to use the program.

Requirements: Poetry

In main.py, you can choose which text file to compress by editing the og_path variable. Note that the program only supports ASCII-data. The compressed data will be saved into binfile.bin located in the project's root directory. The program will print the compression ratio achieved using each algorithm.

Install dependencies:

```bash
poetry install
```

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
