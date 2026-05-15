"""Command-line interface for routemap."""

import argparse
import sys
from pathlib import Path

from routemap.parsers import get_parser, SUPPORTED_FRAMEWORKS
from routemap.output.renderer import render


def build_parser() -> argparse.ArgumentParser:
    """Build and return the argument parser."""
    parser = argparse.ArgumentParser(
        prog="routemap",
        description="Generate a visual map of API routes from Express or FastAPI codebases.",
    )
    parser.add_argument(
        "path",
        type=str,
        help="Path to the file or directory to analyze.",
    )
    parser.add_argument(
        "-f",
        "--framework",
        type=str,
        required=True,
        choices=[fw.lower() for fw in SUPPORTED_FRAMEWORKS],
        help="Framework to parse (e.g. fastapi, express).",
    )
    parser.add_argument(
        "-o",
        "--output",
        type=str,
        default="text",
        choices=["text", "json", "html"],
        help="Output format (default: text).",
    )
    parser.add_argument(
        "--out-file",
        type=str,
        default=None,
        help="Write output to a file instead of stdout.",
    )
    return parser


def main(argv=None) -> int:
    """Entry point for the CLI. Returns exit code."""
    parser = build_parser()
    args = parser.parse_args(argv)

    target = Path(args.path)
    if not target.exists():
        print(f"error: path '{target}' does not exist.", file=sys.stderr)
        return 1

    try:
        route_parser = get_parser(args.framework)
    except ValueError as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 1

    if target.is_dir():
        routes = route_parser.parse_directory(str(target))
    else:
        routes = route_parser.parse_file(str(target))

    output = render(routes, fmt=args.output)

    if args.out_file:
        out_path = Path(args.out_file)
        out_path.write_text(output, encoding="utf-8")
        print(f"Output written to {out_path}")
    else:
        print(output)

    return 0


if __name__ == "__main__":
    sys.exit(main())
