"""Parser for extracting API routes from FastAPI codebases."""

import re
from dataclasses import dataclass, field
from pathlib import Path
from typing import Optional


HTTP_METHODS = {"get", "post", "put", "patch", "delete", "options", "head"}

ROUTE_PATTERN = re.compile(
    r"@(?P<router>\w+)\.(?P<method>" + "|".join(HTTP_METHODS) + r")\("
    r"[\s]*[\'\"](?P<path>[^\'\"]+)[\'\"]",
    re.IGNORECASE,
)

FUNCTION_PATTERN = re.compile(
    r"async\s+def\s+(?P<name>\w+)|def\s+(?P<name2>\w+)"
)


@dataclass
class Route:
    method: str
    path: str
    handler: Optional[str]
    source_file: str
    line_number: int
    tags: list[str] = field(default_factory=list)

    def to_dict(self) -> dict:
        return {
            "method": self.method.upper(),
            "path": self.path,
            "handler": self.handler,
            "source_file": self.source_file,
            "line_number": self.line_number,
            "tags": self.tags,
        }


def parse_file(filepath: str | Path) -> list[Route]:
    """Parse a single Python file and extract FastAPI route definitions."""
    filepath = Path(filepath)
    routes: list[Route] = []

    source = filepath.read_text(encoding="utf-8")
    lines = source.splitlines()

    for line_num, line in enumerate(lines, start=1):
        match = ROUTE_PATTERN.search(line)
        if not match:
            continue

        method = match.group("method").lower()
        path = match.group("path")
        handler = None

        # Look ahead for the function definition
        for lookahead in lines[line_num: line_num + 5]:
            fn_match = FUNCTION_PATTERN.search(lookahead)
            if fn_match:
                handler = fn_match.group("name") or fn_match.group("name2")
                break

        routes.append(
            Route(
                method=method,
                path=path,
                handler=handler,
                source_file=str(filepath),
                line_number=line_num,
            )
        )

    return routes


def parse_directory(directory: str | Path) -> list[Route]:
    """Recursively parse all Python files in a directory."""
    directory = Path(directory)
    all_routes: list[Route] = []

    for py_file in sorted(directory.rglob("*.py")):
        try:
            all_routes.extend(parse_file(py_file))
        except (OSError, UnicodeDecodeError):
            continue

    return all_routes
