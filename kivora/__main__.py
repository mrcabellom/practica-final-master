"""Command line entry point.

    python -m kivora --inbox data/inbox --reference data/reference --out output

The three options and their defaults are the interface the platform team
uses to run the pipeline: do not rename them.
"""

import argparse
import sys
from pathlib import Path

from kivora.pipeline import run


def main(argv=None):
    parser = argparse.ArgumentParser(prog="python -m kivora",
                                     description="Pipeline diario de Kivora.")
    parser.add_argument("--inbox", type=Path, default=Path("data/inbox"),
                        help="carpeta con una subcarpeta por día (por defecto: data/inbox)")
    parser.add_argument("--reference", type=Path, default=Path("data/reference"),
                        help="carpeta con las tablas de referencia (por defecto: data/reference)")
    parser.add_argument("--out", type=Path, default=Path("output"),
                        help="carpeta de salida (por defecto: output)")
    args = parser.parse_args(argv)
    sys.stdout.reconfigure(encoding="utf-8")
    run(args.inbox, args.reference, args.out)
    return 0


if __name__ == "__main__":
    sys.exit(main())
