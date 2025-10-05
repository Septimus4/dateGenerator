# Command Line Usage

After installing the package, the `date-generator` command becomes available. The CLI mirrors the Python API and exposes parameters that are useful when building password wordlists or quick test fixtures.

## Basic usage

Generate ISO formatted dates between 2000 and 2001:

```bash
date-generator --start 2000 --end 2001 --preset ymd
```

Output includes the end year and prints directly to `stdout`.

## Customising separators and casing

```bash
date-generator --start 1999 --end 1999 --preset mdy --separator "/" --case upper
```

This prints `MM/DD/YYYY` in uppercase, which is particularly handy when working with systems that normalise user input.

## Filtering months or days

When testing a seasonal promotion or a leap-day edge case you might not want every day of the year:

```bash
date-generator --start 2024 --end 2024 --months 2 --days 29
```

Only February 29th is emitted.

Multiple values can be passed for both `--months` and `--days`.

## Prefixes, suffixes, and reversing order

Append context or reverse chronological order to target the latest dates first:

```bash
date-generator --start 2018 --end 2024 --preset dmys --separator . --prefix corp- --suffix "!" --reverse
```

## Working with custom patterns

The `--pattern` option accepts any valid `strftime` string and overrides the preset/ separator configuration:

```bash
date-generator --start 1990 --end 1990 --pattern "%d%b%Y" --case lower
```

Result: `01jan1990`, `02jan1990`, etc.

## Saving to a file

Use `--output` to write values to disk and choose a newline when targeting Windows tools:

```bash
date-generator --start 2000 --end 2005 --preset ymd --output wordlists/dates.txt --newline "\r\n"
```

## Discovering presets

List all bundled presets along with examples:

```bash
date-generator --list-presets
```

See `date-generator --help` for the full list of options.
