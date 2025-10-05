from __future__ import annotations

import pytest

from date_generator.core import DateGeneratorError, parse_format_spec


def test_parse_format_spec_accepts_partial_components() -> None:
    chunks = parse_format_spec("MMDD")
    assert chunks == ("M", "D")


@pytest.mark.parametrize(
    ("spec", "expected"),
    [
        ("", "format string must not be empty"),
        ("QQ", "format may only contain Y, M, and D characters"),
        ("YYYYY", "Y groups must be either 'YY' or 'YYYY'"),
        ("MMM", "M groups must be exactly 'MM'"),
    ],
)
def test_parse_format_spec_invalid_inputs(spec: str, expected: str) -> None:
    with pytest.raises(DateGeneratorError) as exc:
        parse_format_spec(spec)
    assert expected in str(exc.value)
