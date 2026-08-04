"""CLI wrapper around darkwatch.s1_prep.pipeline."""

from __future__ import annotations

import sys
from pathlib import Path

# Allow running without installing the package.
REPO_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO_ROOT))

from darkwatch.s1_prep.pipeline import main

if __name__ == "__main__":
    sys.exit(main())
