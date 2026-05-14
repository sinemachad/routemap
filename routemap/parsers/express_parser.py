import re
from pathlib import Path
from dataclasses import dataclass, field
from typing import Optional


@dataclass
class Route:
    method: str
    path: str
    handler: Optional[str] = None
    file: Optional[str] = None

    def to_dict(self) -> dict:
        return {
            "method": self.method,
            "path": self.path,
            "handler": self.handler,
            "file": self.file,
        }


# Matches: router.get('/path', handler) or app.post('/path', handler)
ROUTE_PATTERN = re.compile(
    r"(?:app|router)\.(get|post|put|patch|delete|options|head)\s*\(\s*['\"]([^'\"]+)['\"]"
    r"(?:\s*,\s*([\w.]+))?",
    re.IGNORECASE,
)


def parse_file(filepath: str) -> list[Route]:
    """Parse an Express.js file and return a list of Route objects."""
    routes = []
    path = Path(filepath)

    try:
        content = path.read_text(encoding="utf-8")
    except (OSError, UnicodeDecodeError):
        return routes

    for match in ROUTE_PATTERN.finditer(content):
        method = match.group(1).upper()
        route_path = match.group(2)
        handler = match.group(3) if match.group(3) else None
        routes.append(
            Route(method=method, path=route_path, handler=handler, file=str(path))
        )

    return routes


def parse_directory(directory: str, extensions: tuple[str, ...] = (".js", ".ts")) -> list[Route]:
    """Recursively parse all Express route files in a directory."""
    all_routes = []
    base = Path(directory)

    for ext in extensions:
        for filepath in base.rglob(f"*{ext}"):
            all_routes.extend(parse_file(str(filepath)))

    return all_routes
