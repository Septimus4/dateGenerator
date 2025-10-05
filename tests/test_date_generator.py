from __future__ import annotations

from pathlib import Path

import pytest

from date_generator import DateGenerator, generate_dates
from date_generator.cli import FORMAT_SAMPLES, run_from_args
from date_generator.core import DateGeneratorError


def test_generate_dates_default_order():
    result = generate_dates(start_year=2024, end_year=2024, format="YYYYMMDD", separator="-")
    assert result[0] == "2024-01-01"
    assert result[-1] == "2024-12-31"
    assert len(result) == 366  # leap year


def test_reverse_order_and_filters(tmp_path: Path):
    generator = DateGenerator(
        start_year=2023,
        end_year=2024,
        format="DDMMYY",
        separator="/",
        reverse=True,
        months=[1, 2],
        days=[1, 29, 31],
        prefix="corp-",
        suffix="!",
    )
    values = generator.generate_to_list()
    assert values[0].startswith("corp-29/02/24")
    assert values[-1].endswith("01/01/23!")
    output_file = generator.write(tmp_path / "dates.txt")
    assert output_file.read_text(encoding="utf-8").splitlines()[0] == values[0]


def test_generate_dates_month_only():
    values = generate_dates(
        start_year=2024,
        end_year=2024,
        format="MM",
        months=[1, 2, 3],
        days=[1],
    )
    assert values == ["01", "02", "03"]


def test_custom_pattern_lowercase():
    generator = DateGenerator(start_year=1990, end_year=1990, custom_pattern="%d%b%Y", case="lower")
    values = generator.generate_to_list()
    assert values[0] == "01jan1990"
    assert values[1] == "02jan1990"
    assert len(values) == 365


def test_invalid_configuration_raises():
    with pytest.raises(DateGeneratorError):
        DateGenerator(start_year=2024, end_year=2023)

    with pytest.raises(DateGeneratorError):
        DateGenerator(start_year=2020, end_year=2021, format="invalid")

    with pytest.raises(DateGeneratorError):
        DateGenerator(start_year=2020, end_year=2021, case="title")


def test_cli_prints_to_stdout(capsys):
    exit_code = run_from_args(
        [
            "-s",
            "2024",
            "-e",
            "2024",
            "-f",
            "MMDDYYYY",
            "-S",
            "-",
            "-m",
            "1",
            "-d",
            "15",
        ]
    )
    assert exit_code == 0
    captured = capsys.readouterr()
    assert "01-15-2024" in captured.out.splitlines()


def test_cli_list_formats(capsys):
    exit_code = run_from_args(["--list-formats"])
    assert exit_code == 0
    output = capsys.readouterr().out
    for key in FORMAT_SAMPLES:
        assert key in output


def test_cli_short_flags_and_prefix_suffix(capsys):
    exit_code = run_from_args(
        [
            "-s",
            "2024",
            "-e",
            "2024",
            "-f",
            "MMDD",
            "-P",
            "pre-",
            "-X",
            "post",
            "-r",
            "-m",
            "1",
            "-d",
            "1",
        ]
    )
    assert exit_code == 0
    captured = capsys.readouterr().out.splitlines()
    assert captured[0].startswith("pre-")
    assert captured[0].endswith("post")


def test_cli_writes_file(tmp_path: Path):
    file_path = tmp_path / "out.txt"
    exit_code = run_from_args(
        [
            "--start",
            "2024",
            "--end",
            "2024",
            "--format",
            "YYMMDD",
            "--output",
            str(file_path),
            "--newline",
            "\r\n",
        ]
    )
    assert exit_code == 0
    content = file_path.read_bytes()
    assert content.startswith(b"24")
    assert b"\r\n" in content
