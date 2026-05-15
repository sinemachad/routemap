"""Renders parsed routes into various output formats."""

from typing import List, Dict, Any
import json


HTTP_METHOD_COLORS = {
    "GET": "#61affe",
    "POST": "#49cc90",
    "PUT": "#fca130",
    "PATCH": "#50e3c2",
    "DELETE": "#f93e3e",
    "OPTIONS": "#0d5aa7",
    "HEAD": "#9012fe",
}

DEFAULT_COLOR = "#999999"


def render_json(routes: List[Dict[str, Any]], indent: int = 2) -> str:
    """Render routes as a formatted JSON string."""
    return json.dumps(routes, indent=indent)


def render_text(routes: List[Dict[str, Any]]) -> str:
    """Render routes as a plain-text table."""
    if not routes:
        return "No routes found."

    lines = []
    header = f"{'METHOD':<10} {'PATH':<40} {'HANDLER'}"
    lines.append(header)
    lines.append("-" * len(header))

    for route in routes:
        method = route.get("method", "UNKNOWN").upper()
        path = route.get("path", "/")
        handler = route.get("handler", "")
        lines.append(f"{method:<10} {path:<40} {handler}")

    return "\n".join(lines)


def render_html(routes: List[Dict[str, Any]], title: str = "API Route Map") -> str:
    """Render routes as a self-contained HTML page."""
    rows = ""
    for route in routes:
        method = route.get("method", "UNKNOWN").upper()
        path = route.get("path", "/")
        handler = route.get("handler", "")
        color = HTTP_METHOD_COLORS.get(method, DEFAULT_COLOR)
        rows += (
            f"<tr>"
            f"<td><span class='badge' style='background:{color}'>{method}</span></td>"
            f"<td><code>{path}</code></td>"
            f"<td>{handler}</td>"
            f"</tr>\n"
        )

    return f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <title>{title}</title>
  <style>
    body {{ font-family: sans-serif; padding: 2rem; background: #f9f9f9; }}
    h1 {{ color: #333; }}
    table {{ border-collapse: collapse; width: 100%; background: #fff; }}
    th, td {{ text-align: left; padding: 0.6rem 1rem; border-bottom: 1px solid #eee; }}
    th {{ background: #f0f0f0; font-weight: 600; }}
    .badge {{ color: #fff; padding: 2px 8px; border-radius: 4px;
              font-size: 0.75rem; font-weight: bold; }}
    code {{ background: #f0f0f0; padding: 2px 6px; border-radius: 3px; }}
  </style>
</head>
<body>
  <h1>{title}</h1>
  <table>
    <thead><tr><th>Method</th><th>Path</th><th>Handler</th></tr></thead>
    <tbody>
{rows}    </tbody>
  </table>
</body>
</html>"""


SUPPORTED_FORMATS = ["json", "text", "html"]


def render(routes: List[Dict[str, Any]], fmt: str = "text", **kwargs) -> str:
    """Dispatch rendering to the appropriate format function."""
    fmt = fmt.lower()
    if fmt == "json":
        return render_json(routes, **kwargs)
    elif fmt == "html":
        return render_html(routes, **kwargs)
    elif fmt == "text":
        return render_text(routes)
    else:
        raise ValueError(f"Unsupported format '{fmt}'. Choose from: {SUPPORTED_FORMATS}")
