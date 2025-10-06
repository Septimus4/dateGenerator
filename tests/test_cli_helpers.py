from __future__ import annotations

import argparse
from pathlib import Path

import pytest

from chronogen.cli import (
    PositiveIntAction,
    main,
    parse_format,
    parse_newline,
    run_from_args,
)
from chronogen.core import DateGeneratorError


@pytest.mark.parametrize(
    ("value", "expected"),
    [("lf", "\n"), ("crlf", "\r\n"), ("\\n", "\n"), ("\r\n", "\r\n")],
)
def test_parse_newline_accepts_aliases(value: str, expected: str) -> None:
    assert parse_newline(value) == expected


def test_parse_newline_rejects_unknown_values() -> None:
    with pytest.raises(argparse.ArgumentTypeError):
        parse_newline("invalid")


def test_positive_int_action_validates_values() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--numbers", action=PositiveIntAction)
    namespace = parser.parse_args(["--numbers", "1", "2"])
    assert namespace.numbers == [1, 2]
    with pytest.raises(SystemExit):
        parser.parse_args(["--numbers", "0"])


@pytest.mark.parametrize("format_spec", ["MM", "DD", "YYYYMM", "YYMMDD"])
def test_parse_format_accepts_variants(format_spec: str) -> None:
    assert parse_format(format_spec) == format_spec.upper()


@pytest.mark.parametrize("format_spec", ["", "QQ", "YYYYY"])
def test_parse_format_rejects_invalid(format_spec: str) -> None:
    with pytest.raises(argparse.ArgumentTypeError):
        parse_format(format_spec)


def test_run_from_args_respects_custom_pattern(tmp_path: Path) -> None:
    path = tmp_path / "out.txt"
    exit_code = run_from_args(
        [
            "-s",
            "2024",
            "-e",
            "2024",
            "-f",
            "MMDD",
            "-p",
            "%b",
            "-o",
            str(path),
        ]
    )
    assert exit_code == 0
    content = path.read_text(encoding="utf-8").splitlines()
    assert content[0].isalpha()


def test_run_from_args_requires_start_end_when_generating() -> None:
    with pytest.raises(SystemExit):
        run_from_args(["-s", "2024"])


def test_main_handles_core_errors(monkeypatch: pytest.MonkeyPatch) -> None:
    def broken_config(*args, **kwargs):  # type: ignore[unused-argument]
        raise DateGeneratorError("boom")

    monkeypatch.setattr("chronogen.cli.DateGenerator", broken_config)
    monkeypatch.setattr("chronogen.cli.sys.argv", ["chronogen", "-s", "2024", "-e", "2024"])
    exit_code = main()
    assert exit_code == 2
