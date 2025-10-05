"""Allow running ``python -m date_generator``."""
from .cli import main

if __name__ == "__main__":
    raise SystemExit(main())
