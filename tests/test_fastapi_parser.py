"""Tests for the FastAPI route parser."""

import textwrap
from pathlib import Path

import pytest

from routemap.parsers.fastapi_parser import Route, parse_directory, parse_file


@pytest.fixture()
def sample_fastapi_file(tmp_path: Path) -> Path:
    code = textwrap.dedent("""\
        from fastapi import FastAPI, APIRouter

        app = FastAPI()
        router = APIRouter()

        @app.get("/health")
        async def health_check():
            return {"status": "ok"}

        @router.post("/users")
        async def create_user():
            pass

        @router.put("/users/{user_id}")
        def update_user(user_id: int):
            pass

        @router.delete("/users/{user_id}")
        async def delete_user(user_id: int):
            pass
    """)
    file = tmp_path / "main.py"
    file.write_text(code)
    return file


def test_parse_file_returns_correct_count(sample_fastapi_file: Path):
    routes = parse_file(sample_fastapi_file)
    assert len(routes) == 4


def test_parse_file_methods(sample_fastapi_file: Path):
    routes = parse_file(sample_fastapi_file)
    methods = {r.method for r in routes}
    assert methods == {"get", "post", "put", "delete"}


def test_parse_file_paths(sample_fastapi_file: Path):
    routes = parse_file(sample_fastapi_file)
    paths = {r.path for r in routes}
    assert "/health" in paths
    assert "/users" in paths
    assert "/users/{user_id}" in paths


def test_parse_file_handler_names(sample_fastapi_file: Path):
    routes = parse_file(sample_fastapi_file)
    handlers = {r.handler for r in routes}
    assert "health_check" in handlers
    assert "create_user" in handlers
    assert "update_user" in handlers
    assert "delete_user" in handlers


def test_route_to_dict(sample_fastapi_file: Path):
    routes = parse_file(sample_fastapi_file)
    d = routes[0].to_dict()
    assert set(d.keys()) == {"method", "path", "handler", "source_file", "line_number", "tags"}
    assert d["method"] == d["method"].upper()


def test_parse_directory(tmp_path: Path, sample_fastapi_file: Path):
    # sample_fastapi_file is already in tmp_path
    routes = parse_directory(tmp_path)
    assert len(routes) == 4


def test_parse_directory_multiple_files(tmp_path: Path, sample_fastapi_file: Path):
    extra = tmp_path / "extra.py"
    extra.write_text("@app.get('/ping')\nasync def ping(): pass\n")
    routes = parse_directory(tmp_path)
    assert len(routes) == 5


def test_parse_empty_file(tmp_path: Path):
    empty = tmp_path / "empty.py"
    empty.write_text("")
    routes = parse_file(empty)
    assert routes == []
