# Date Generator

Date Generator is a lightweight toolkit for generating date-based wordlists and performing quick calendar automations.  It can be used as a Python library, a command line interface, or a standalone script.

## Highlights

- **Python package first** – import `date_generator` in any project and access the `DateGenerator` class or helper functions.
- **Flexible formatting** – customise output with symbolic format templates or bring your own `strftime` pattern.
- **Wordlist friendly** – apply prefixes, suffixes, casing rules, and chronological order suitable for penetration testing.
- **CLI ready** – install the package and run `date-generator` for on-the-fly date generation.

## Getting started

1. Install the package (after building or from PyPI):

   ```bash
   pip install date-generator
   ```

2. Generate values directly from the command line:

   ```bash
   date-generator --start 1990 --end 1995 --format DDMMYY --separator "/" --prefix user-
   ```

3. Or import the library in Python:

   ```python
   from date_generator import DateGenerator

   generator = DateGenerator(start_year=1990, end_year=1995, format="YYYYMMDD")
   for value in generator.generate():
       print(value)
   ```

Explore the rest of the documentation for advanced usage and development workflows.
