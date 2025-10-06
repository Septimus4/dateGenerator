# Command Line Usage

After installing the package, the `chronogen` command becomes available. The CLI mirrors the Python API and exposes parameters that are useful when building password wordlists or quick test fixtures.

## Basic usage

Generate ISO formatted dates between 2000 and 2001:

```bash
chronogen -s 2000 -e 2001 -f YYYYMMDD
```

Output includes the end year and prints directly to `stdout`.

## Customising separators and casing

```bash
chronogen -s 1999 -e 1999 -f MMDDYYYY -S "/" --case upper
```

This prints `MM/DD/YYYY` in uppercase, which is particularly handy when working with systems that normalise user input.

## Filtering months or days

When testing a seasonal promotion or a leap-day edge case you might not want every day of the year:

```bash
chronogen --start 2024 --end 2024 --months 2 --days 29
```

Only February 29th is emitted.

Multiple values can be passed for both `--months` and `--days`.

## Prefixes, suffixes, and reversing order

Append context or reverse chronological order to target the latest dates first:

```bash
chronogen -s 2018 -e 2024 -f DDMMYY -S . -P corp- --suffix "!" -r
```

## Working with custom patterns

The `--pattern` option accepts any valid `strftime` string and overrides the format template and separator configuration:

```bash
chronogen --start 1990 --end 1990 --pattern "%d%b%Y" --case lower
```

Result: `01jan1990`, `02jan1990`, etc.

## Saving to a file

Use `--output` (or `-o`) to write values to disk and choose a newline when targeting Windows tools:

```bash
chronogen -s 2000 -e 2005 -f YYYYMMDD -o wordlists/dates.txt -n "\r\n"
```

## Discovering format templates

List suggested format templates along with examples:

```bash
chronogen --list-formats
```
These strings are made up of contiguous `Y`, `M`, and `D` blocks. Use `YY` for short years and `YYYY` for full years. Each component is optional, so formats like `MM`, `DD`, or `MMDD` are valid. See `chronogen --help` for the full list of options and short flag aliases.
