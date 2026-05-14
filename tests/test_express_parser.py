import os
import pytest
from textwrap import dedent
from routemap.parsers.express_parser import parse_file, parse_directory, Route


@pytest.fixture
def sample_express_file(tmp_path):
    content = dedent("""
        const express = require('express');
        const router = express.Router();

        router.get('/users', getUsers);
        router.post('/users', createUser);
        router.get('/users/:id', getUserById);
        router.put('/users/:id', updateUser);
        router.delete('/users/:id', deleteUser);
        router.patch('/users/:id/status', patchUserStatus);

        module.exports = router;
    """)
    file = tmp_path / "users.js"
    file.write_text(content)
    return str(file)


def test_parse_file_returns_correct_count(sample_express_file):
    routes = parse_file(sample_express_file)
    assert len(routes) == 6


def test_parse_file_methods(sample_express_file):
    routes = parse_file(sample_express_file)
    methods = [r.method for r in routes]
    assert "GET" in methods
    assert "POST" in methods
    assert "PUT" in methods
    assert "DELETE" in methods
    assert "PATCH" in methods


def test_parse_file_paths(sample_express_file):
    routes = parse_file(sample_express_file)
    paths = [r.path for r in routes]
    assert "/users" in paths
    assert "/users/:id" in paths
    assert "/users/:id/status" in paths


def test_parse_file_handlers(sample_express_file):
    routes = parse_file(sample_express_file)
    handlers = [r.handler for r in routes]
    assert "getUsers" in handlers
    assert "createUser" in handlers


def test_parse_file_sets_file_attribute(sample_express_file):
    routes = parse_file(sample_express_file)
    for route in routes:
        assert route.file == sample_express_file


def test_parse_file_returns_route_instances(sample_express_file):
    routes = parse_file(sample_express_file)
    for route in routes:
        assert isinstance(route, Route)


def test_to_dict(sample_express_file):
    routes = parse_file(sample_express_file)
    d = routes[0].to_dict()
    assert "method" in d
    assert "path" in d
    assert "handler" in d
    assert "file" in d


def test_parse_file_nonexistent():
    routes = parse_file("/nonexistent/path/file.js")
    assert routes == []


def test_parse_directory(tmp_path):
    (tmp_path / "routes").mkdir()
    (tmp_path / "routes" / "auth.js").write_text(
        "app.post('/login', loginHandler);\napp.post('/logout', logoutHandler);\n"
    )
    (tmp_path / "routes" / "items.ts").write_text(
        "router.get('/items', listItems);\n"
    )
    routes = parse_directory(str(tmp_path))
    assert len(routes) == 3


def test_parse_directory_empty(tmp_path):
    routes = parse_directory(str(tmp_path))
    assert routes == []
