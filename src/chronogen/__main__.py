"""Allow running ``python -m chronogen``."""

from .cli import main

if __name__ == "__main__":
    raise SystemExit(main())
