"""Compatibility wrapper allowing ``python date_generator.py`` execution."""

from date_generator.cli import main

if __name__ == "__main__":
    raise SystemExit(main())
