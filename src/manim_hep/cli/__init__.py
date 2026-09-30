"""The ``manim-hep`` command line."""

from __future__ import annotations

import argparse
import sys

from manim_hep import __version__


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="manim-hep",
        description="Tools for making HEP animations with Manim Community Edition.",
    )
    parser.add_argument("--version", action="version", version=f"manim-hep {__version__}")
    parser.add_subparsers(dest="command", metavar="COMMAND")
    return parser


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    if args.command is None:
        parser.print_help()
        return 0
    return args.func(args)


if __name__ == "__main__":
    sys.exit(main())
