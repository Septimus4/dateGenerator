"""Command line interface for the date generator package."""
from __future__ import annotations

import argparse
import sys
from pathlib import Path
from typing import Sequence

from .core import FORMAT_PRESETS, DateGenerator, DateGeneratorConfig, DateGeneratorError


class PositiveIntAction(argparse.Action):
    """Argparse action that converts arguments to positive integers."""

    def __call__(
        self,
        parser: argparse.ArgumentParser,
        namespace: argparse.Namespace,
        values: Sequence[str] | str,
        option_string: str | None = None,
    ) -> None:
        if isinstance(values, Sequence) and not isinstance(values, (str, bytes)):
            converted = [self._convert(value, parser, option_string) for value in values]
        else:
            converted = self._convert(values, parser, option_string)
        setattr(namespace, self.dest, converted)

    def _convert(
        self, value: str, parser: argparse.ArgumentParser, option_string: str | None
    ) -> int:
        try:
            value_int = int(value)
        except (TypeError, ValueError):
            parser.error(f"{option_string or ''} expects integer values")
        if value_int <= 0:
            parser.error(f"{option_string or ''} values must be positive integers")
        return value_int


def build_parser() -> argparse.ArgumentParser:
    choices = {key: preset.description for key, preset in FORMAT_PRESETS.items()}
    parser = argparse.ArgumentParser(
        prog="date-generator",
        description="Generate date-based wordlists for pentesting and automation.",
    )
    parser.add_argument("--start", type=int, help="Starting year (inclusive)")
    parser.add_argument("--end", type=int, help="Ending year (inclusive)")
    parser.add_argument(
        "--preset",
        choices=sorted(choices),
        default="ymd",
        help="Predefined format for output dates",
    )
    parser.add_argument(
        "--separator",
        default="",
        help="String inserted between date parts (ignored for custom patterns)",
    )
    parser.add_argument(
        "--pattern",
        dest="custom_pattern",
        help="Custom strftime pattern overriding preset (e.g. '%d%b%Y')",
    )
    parser.add_argument(
        "--months",
        nargs="+",
        action=PositiveIntAction,
        metavar="MONTH",
        help="Restrict generation to specific months (1-12)",
    )
    parser.add_argument(
        "--days",
        nargs="+",
        action=PositiveIntAction,
        metavar="DAY",
        help="Restrict generation to specific days of the month (1-31)",
    )
    parser.add_argument("--prefix", default="", help="Prefix to prepend to every value")
    parser.add_argument("--suffix", default="", help="Suffix appended to every value")
    parser.add_argument(
        "--case",
        choices=["lower", "upper"],
        help="Apply lower or upper casing to the generated values",
    )
    parser.add_argument(
        "--reverse",
        action="store_true",
        help="Generate dates in reverse chronological order",
    )
    parser.add_argument(
        "--output",
        type=Path,
        help="Optional file path where the values will be written",
    )
    parser.add_argument(
        "--newline",
        default="\n",
        choices=["\n", "\r\n"],
        help="Line ending to use when writing to a file",
    )
    parser.add_argument(
        "--list-presets",
        action="store_true",
        help="Display preset descriptions and exit",
    )
    return parser


def run_from_args(args: Sequence[str] | None = None) -> int:
    parser = build_parser()
    namespace = parser.parse_args(args=args)
    if namespace.list_presets:
        for key in sorted(FORMAT_PRESETS):
            preset = FORMAT_PRESETS[key]
            print(f"{preset.key}: {preset.description}")
        return 0
    if namespace.start is None or namespace.end is None:
        parser.error("--start and --end are required unless --list-presets is provided")
    config = DateGeneratorConfig(
        start_year=namespace.start,
        end_year=namespace.end,
        preset=namespace.preset,
        separator=namespace.separator,
        custom_pattern=namespace.custom_pattern,
        months=namespace.months,
        days=namespace.days,
        prefix=namespace.prefix,
        suffix=namespace.suffix,
        case=namespace.case,
        reverse=namespace.reverse,
    )
    generator = DateGenerator(config)

    if namespace.output:
        generator.write(namespace.output, newline=namespace.newline)
    else:
        for value in generator.generate():
            print(value)
    return 0


def main() -> int:
    try:
        return run_from_args()
    except DateGeneratorError as exc:
        print(str(exc), file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
