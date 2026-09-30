"""The ``manim-hep`` command line."""

from __future__ import annotations

import argparse
import sys

from manim_hep import __version__


def build_parser() -> argparse.ArgumentParser:
    from manim_hep.cli import lint, render, seam

    parser = argparse.ArgumentParser(
        prog="manim-hep",
        description="Tools for making HEP animations with Manim Community Edition.",
    )
    parser.add_argument("--version", action="version", version=f"manim-hep {__version__}")
    sub = parser.add_subparsers(dest="command", metavar="COMMAND")
    for module in (render, lint, seam):
        module.add_parser(sub)
    return parser


def main(argv: list[str] | None = None) -> int:
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(errors="replace")
    parser = build_parser()
    args = parser.parse_args(argv)
    if args.command is None:
        parser.print_help()
        return 0
    return args.func(args)


if __name__ == "__main__":
    sys.exit(main())
