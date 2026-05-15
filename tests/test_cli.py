"""Tests for the routemap CLI."""

import json
import textwrap
from pathlib import Path

import pytest

from routemap.cli import main, build_parser


@pytest.fixture()
def fastapi_file(tmp_path: Path) -> Path:
    content = textwrap.dedent("""
        from fastapi import FastAPI
        app = FastAPI()

        @app.get("/items")
        def list_items():
            pass

        @app.post("/items")
        def create_item():
            pass
    """)
    f = tmp_path / "main.py"
    f.write_text(content)
    return f


def test_build_parser_returns_parser():
    parser = build_parser()
    assert parser is not None
    assert parser.prog == "routemap"


def test_main_missing_path_exits_nonzero():
    result = main(["nonexistent_path", "--framework", "fastapi"])
    assert result == 1


def test_main_invalid_framework_exits_nonzero(fastapi_file: Path):
    result = main([str(fastapi_file), "--framework", "django"])
    assert result != 0


def test_main_text_output_exits_zero(fastapi_file: Path, capsys):
    result = main([str(fastapi_file), "--framework", "fastapi", "--output", "text"])
    assert result == 0
    captured = capsys.readouterr()
    assert "/items" in captured.out


def test_main_json_output_is_valid_json(fastapi_file: Path, capsys):
    result = main([str(fastapi_file), "--framework", "fastapi", "--output", "json"])
    assert result == 0
    captured = capsys.readouterr()
    data = json.loads(captured.out)
    assert isinstance(data, list)
    assert len(data) == 2


def test_main_html_output_contains_html_tags(fastapi_file: Path, capsys):
    result = main([str(fastapi_file), "--framework", "fastapi", "--output", "html"])
    assert result == 0
    captured = capsys.readouterr()
    assert "<html" in captured.out


def test_main_writes_to_file(fastapi_file: Path, tmp_path: Path):
    out_file = tmp_path / "routes.txt"
    result = main([
        str(fastapi_file),
        "--framework", "fastapi",
        "--output", "text",
        "--out-file", str(out_file),
    ])
    assert result == 0
    assert out_file.exists()
    assert "/items" in out_file.read_text()


def test_main_directory_input(tmp_path: Path, capsys):
    (tmp_path / "routes.py").write_text(
        "from fastapi import FastAPI\napp = FastAPI()\n"
        "@app.get('/health')\ndef health(): pass\n"
    )
    result = main([str(tmp_path), "--framework", "fastapi"])
    assert result == 0
    captured = capsys.readouterr()
    assert "/health" in captured.out
