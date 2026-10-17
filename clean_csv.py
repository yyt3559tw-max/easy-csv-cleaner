#!/usr/bin/env python3
"""Clean CSV files using only the Python standard library."""
import argparse
import csv
from pathlib import Path


def clean_csv(source: Path, destination: Path, encoding: str = 'utf-8-sig') -> dict:
    if source.resolve() == destination.resolve():
        raise ValueError('Input and output files must be different.')
    if not source.is_file():
        raise FileNotFoundError(f'Input file not found: {source}')
    destination.parent.mkdir(parents=True, exist_ok=True)
    with source.open('r', encoding=encoding, newline='') as stream:
        reader = csv.reader(stream)
        try:
            header = next(reader)
        except StopIteration:
            raise ValueError('Input CSV is empty.') from None
        header = [cell.strip() for cell in header]
        if not any(header):
            raise ValueError('CSV header is blank.')
        width = len(header)
        seen = set()
        cleaned = []
        blank = duplicate = total = 0
        for line_number, row in enumerate(reader, start=2):
            total += 1
            if len(row) != width:
                raise ValueError(f'Row {line_number} has {len(row)} columns; expected {width}.')
            normalized = tuple(cell.strip() for cell in row)
            if not any(normalized):
                blank += 1
                continue
            if normalized in seen:
                duplicate += 1
                continue
            seen.add(normalized)
            cleaned.append(normalized)
    with destination.open('w', encoding=encoding, newline='') as stream:
        writer = csv.writer(stream)
        writer.writerow(header)
        writer.writerows(cleaned)
    return {'rows_read': total, 'rows_written': len(cleaned), 'blank_removed': blank, 'duplicates_removed': duplicate}


def main() -> None:
    parser = argparse.ArgumentParser(description='Clean a CSV file: trim whitespace, remove blank and duplicate rows.')
    parser.add_argument('input', type=Path, help='Path to input CSV')
    parser.add_argument('output', type=Path, help='Path for cleaned CSV (must differ from input)')
    args = parser.parse_args()
    try:
        stats = clean_csv(args.input, args.output)
    except (OSError, UnicodeError, ValueError, csv.Error) as exc:
        parser.exit(1, f'Error: {exc}\n')
    print('Cleaning complete!')
    for key, value in stats.items():
        print(f'{key}: {value}')


if __name__ == '__main__':
    main()
