import tempfile
import unittest
from pathlib import Path
from log_parser import count_errors


def test_count_errors(tmp_path):
    log_file = tmp_path / "test.log"

    log_file.write_text(
        "ERROR DatabaseError: connection failed\n"
        "ERROR TimeoutError: request timed out\n"
        "ERROR DatabaseError: query failed\n"
    )

    result = count_errors(log_file)

    assert result["DatabaseError"] == 2
    assert result["TimeoutError"] == 1
