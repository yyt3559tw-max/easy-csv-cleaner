# easy-csv-cleaner

A beginner-friendly, free, open-source CSV cleaning command-line tool written in Python. No external dependencies.

## Features

- Trims leading and trailing whitespace in headers and cells
- Removes fully blank data rows
- Removes exact duplicate rows after trimming
- Supports UTF-8 CSV files, including Traditional Chinese
- Reports how many rows were processed, removed, and retained
- Rejects inconsistent column counts instead of silently losing data

## Requirements

Python 3.9 or newer.

## Quick start

```bash
python clean_csv.py examples/sample.csv cleaned.csv
```

On Windows, use `py` instead of `python` if needed. The tool creates `cleaned.csv` and prints a summary. Input and output must be different paths. It does not modify your input file.

## Run tests

From the project root:

```bash
python -m unittest discover -s tests -v
```

## Limitations

- CSV only, not Excel `.xlsx` files.
- All fields are treated as text.
- Duplicate matching is case-sensitive.
- Inconsistent row widths cause an error.
- The entire cleaned dataset is held in memory, so very large files may need a future streaming implementation.

## Contributing

Issues and pull requests are welcome. Please describe the problem, include a minimal example (without personal data), and run the tests before submitting a change.

## License

MIT License. See `LICENSE` in the GitHub repository.
