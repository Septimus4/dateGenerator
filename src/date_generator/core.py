"""Core date generation utilities."""
from __future__ import annotations

import calendar
from dataclasses import dataclass
from datetime import date, datetime
from pathlib import Path
from typing import Callable, Iterable, Iterator, Sequence

__all__ = [
    "DateGenerator",
    "DateGeneratorConfig",
    "DateFormat",
    "FORMAT_PRESETS",
    "generate_dates",
]


class DateGeneratorError(ValueError):
    """Base error raised for invalid configuration."""


@dataclass(frozen=True)
class DateFormat:
    """Definition of a supported preset date format."""

    key: str
    description: str
    formatter: Callable[[date, str], str]

    def format(self, value: date, separator: str) -> str:
        """Format ``value`` with ``separator`` using this preset."""

        return self.formatter(value, separator)


def _format_ymd(value: date, separator: str) -> str:
    return f"{value.year:04d}{separator}{value.month:02d}{separator}{value.day:02d}"


def _format_dmy(value: date, separator: str) -> str:
    return f"{value.day:02d}{separator}{value.month:02d}{separator}{value.year:04d}"


def _format_mdy(value: date, separator: str) -> str:
    return f"{value.month:02d}{separator}{value.day:02d}{separator}{value.year:04d}"


def _format_dmys(value: date, separator: str) -> str:
    return f"{value.day:02d}{separator}{value.month:02d}{separator}{value.year % 100:02d}"


def _format_ymds(value: date, separator: str) -> str:
    return f"{value.year % 100:02d}{separator}{value.month:02d}{separator}{value.day:02d}"


def _format_mdys(value: date, separator: str) -> str:
    return f"{value.month:02d}{separator}{value.day:02d}{separator}{value.year % 100:02d}"


FORMAT_PRESETS: dict[str, DateFormat] = {
    "ymd": DateFormat(
        key="ymd",
        description="YYYY{sep}MM{sep}DD (e.g. 20241231)",
        formatter=_format_ymd,
    ),
    "dmy": DateFormat(
        key="dmy",
        description="DD{sep}MM{sep}YYYY (e.g. 31-12-2024)",
        formatter=_format_dmy,
    ),
    "mdy": DateFormat(
        key="mdy",
        description="MM{sep}DD{sep}YYYY (e.g. 12/31/2024)",
        formatter=_format_mdy,
    ),
    "dmys": DateFormat(
        key="dmys",
        description="DD{sep}MM{sep}YY (e.g. 31.12.24)",
        formatter=_format_dmys,
    ),
    "ymds": DateFormat(
        key="ymds",
        description="YY{sep}MM{sep}DD (e.g. 24-12-31)",
        formatter=_format_ymds,
    ),
    "mdys": DateFormat(
        key="mdys",
        description="MM{sep}DD{sep}YY (e.g. 12-31-24)",
        formatter=_format_mdys,
    ),
}


@dataclass
class DateGeneratorConfig:
    """Configuration object for :class:`DateGenerator`."""

    start_year: int
    end_year: int
    preset: str = "ymd"
    separator: str = ""
    custom_pattern: str | None = None
    months: Sequence[int] | None = None
    days: Sequence[int] | None = None
    prefix: str = ""
    suffix: str = ""
    case: str | None = None
    reverse: bool = False

    def normalized(self) -> DateGeneratorConfig:
        """Return a validated, normalized copy of this configuration."""

        if self.start_year > self.end_year:
            raise DateGeneratorError("start_year must be less than or equal to end_year")

        case_normalized = None
        if self.case:
            lowered = self.case.lower()
            if lowered not in {"lower", "upper"}:
                raise DateGeneratorError("case must be 'lower' or 'upper' when provided")
            case_normalized = lowered

        months = self._normalize_int_sequence(self.months, 1, 12, "months")
        days = self._normalize_int_sequence(self.days, 1, 31, "days")

        custom_pattern = self.custom_pattern
        if self.preset not in FORMAT_PRESETS and not custom_pattern:
            choices = ", ".join(sorted(FORMAT_PRESETS))
            raise DateGeneratorError(
                f"preset must be one of {choices} when custom_pattern is not provided"
            )
        if custom_pattern:
            self._validate_pattern(custom_pattern)

        return DateGeneratorConfig(
            start_year=self.start_year,
            end_year=self.end_year,
            preset=self.preset,
            separator=self.separator,
            custom_pattern=custom_pattern,
            months=months,
            days=days,
            prefix=self.prefix,
            suffix=self.suffix,
            case=case_normalized,
            reverse=self.reverse,
        )

    @staticmethod
    def _normalize_int_sequence(
        values: Sequence[int] | None, minimum: int, maximum: int, field: str
    ) -> tuple[int, ...] | None:
        if values is None:
            return None
        normalized: list[int] = []
        for value in values:
            if not minimum <= int(value) <= maximum:
                raise DateGeneratorError(f"{field} must be between {minimum} and {maximum}")
            if int(value) not in normalized:
                normalized.append(int(value))
        return tuple(sorted(normalized))

    @staticmethod
    def _validate_pattern(pattern: str) -> None:
        try:
            datetime(2000, 1, 1).strftime(pattern)
        except ValueError as exc:  # pragma: no cover - only triggered with invalid patterns
            raise DateGeneratorError(f"Invalid custom pattern: {pattern}") from exc


class DateGenerator:
    """Generate formatted date strings for wordlists and automation scripts."""

    def __init__(self, config: DateGeneratorConfig | None = None, /, **kwargs) -> None:
        if config and kwargs:
            raise DateGeneratorError(
                "Provide either a config object or keyword arguments, not both"
            )
        if config is None:
            config = DateGeneratorConfig(**kwargs)
        self.config = config.normalized()

    def __iter__(self) -> Iterator[str]:
        return self.generate()

    def generate(self) -> Iterator[str]:
        """Yield formatted date strings according to the configuration."""

        for current_date in self._iter_dates():
            yield self._format(current_date)

    def generate_to_list(self) -> list[str]:
        """Return all generated date strings in a list."""

        return list(self.generate())

    def write(self, destination: Path | str, newline: str = "\n") -> Path:
        """Write generated date strings to ``destination`` and return the path."""

        path = Path(destination)
        path.parent.mkdir(parents=True, exist_ok=True)
        with path.open("w", encoding="utf-8") as stream:
            for value in self.generate():
                stream.write(value + newline)
        return path

    def _iter_dates(self) -> Iterator[date]:
        months = self.config.months or tuple(range(1, 13))
        days = self.config.days

        if self.config.reverse:
            year_iter: Iterable[int] = range(self.config.end_year, self.config.start_year - 1, -1)

            def iter_months(values: Sequence[int]) -> Iterable[int]:
                return reversed(values)

        else:
            year_iter = range(self.config.start_year, self.config.end_year + 1)

            def iter_months(values: Sequence[int]) -> Iterable[int]:
                return values

        for year in year_iter:
            for month in iter_months(months):
                _, last_day = calendar.monthrange(year, month)
                if days is None:
                    day_iter: Iterable[int]
                    if self.config.reverse:
                        day_iter = range(last_day, 0, -1)
                    else:
                        day_iter = range(1, last_day + 1)
                else:
                    valid_days = [day for day in days if day <= last_day]
                    day_iter = reversed(valid_days) if self.config.reverse else valid_days
                for day in day_iter:
                    yield date(year, month, day)

    def _format(self, value: date) -> str:
        if self.config.custom_pattern:
            formatted = value.strftime(self.config.custom_pattern)
        else:
            formatted = FORMAT_PRESETS[self.config.preset].format(value, self.config.separator)
        if self.config.case == "lower":
            formatted = formatted.lower()
        elif self.config.case == "upper":
            formatted = formatted.upper()
        return f"{self.config.prefix}{formatted}{self.config.suffix}"


def generate_dates(**kwargs) -> list[str]:
    """Convenience wrapper returning generated date strings as a list."""

    return DateGenerator(**kwargs).generate_to_list()
