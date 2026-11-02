#!/usr/bin/env python3
"""Count ERROR events grouped by error type in a text log."""
import argparse
from collections import Counter
from pathlib import Path
import re

# Expected format: 2026-11-02 10:00:00 ERROR DatabaseError: message
ERROR_PATTERN = re.compile(r"\bERROR\s+([A-Za-z_][A-Za-z0-9_]*):")


def count_errors(log_file: Path) -> Counter[str]:
    counts: Counter[str] = Counter()
    with log_file.open("r", encoding="utf-8") as handle:
        for line in handle:
            if match := ERROR_PATTERN.search(line):
                counts[match.group(1)] += 1
    return counts


def main() -> None:
    parser = argparse.ArgumentParser(description="Count errors by type in a log")
    parser.add_argument("log_file", type=Path, help="Path to a log file")
    args = parser.parse_args()
    try:
        counts = count_errors(args.log_file)
    except OSError as exc:
        parser.exit(1, f"Could not read log file: {exc}\n")
    print(f"Total errors: {sum(counts.values())}")
    for error_type, count in sorted(counts.items()):
        print(f"{error_type}: {count}")


if __name__ == "__main__":
    main()
