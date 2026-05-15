"""Tests for routemap.output.renderer."""

import json
import pytest
from routemap.output.renderer import (
    render,
    render_json,
    render_text,
    render_html,
    SUPPORTED_FORMATS,
)


SAMPLE_ROUTES = [
    {"method": "GET", "path": "/users", "handler": "get_users"},
    {"method": "POST", "path": "/users", "handler": "create_user"},
    {"method": "DELETE", "path": "/users/{id}", "handler": "delete_user"},
]


# ── render_json ──────────────────────────────────────────────────────────────

def test_render_json_returns_valid_json():
    result = render_json(SAMPLE_ROUTES)
    parsed = json.loads(result)
    assert isinstance(parsed, list)
    assert len(parsed) == 3


def test_render_json_contains_all_fields():
    result = json.loads(render_json(SAMPLE_ROUTES))
    assert result[0]["method"] == "GET"
    assert result[1]["path"] == "/users"
    assert result[2]["handler"] == "delete_user"


def test_render_json_empty_routes():
    result = render_json([])
    assert json.loads(result) == []


# ── render_text ──────────────────────────────────────────────────────────────

def test_render_text_contains_methods():
    result = render_text(SAMPLE_ROUTES)
    assert "GET" in result
    assert "POST" in result
    assert "DELETE" in result


def test_render_text_contains_paths():
    result = render_text(SAMPLE_ROUTES)
    assert "/users" in result
    assert "/users/{id}" in result


def test_render_text_contains_handlers():
    result = render_text(SAMPLE_ROUTES)
    assert "get_users" in result
    assert "create_user" in result


def test_render_text_empty_routes():
    result = render_text([])
    assert result == "No routes found."


# ── render_html ──────────────────────────────────────────────────────────────

def test_render_html_is_valid_html():
    result = render_html(SAMPLE_ROUTES)
    assert result.strip().startswith("<!DOCTYPE html>")
    assert "</html>" in result


def test_render_html_contains_routes():
    result = render_html(SAMPLE_ROUTES)
    assert "/users" in result
    assert "get_users" in result
    assert "create_user" in result


def test_render_html_contains_method_badges():
    result = render_html(SAMPLE_ROUTES)
    assert "GET" in result
    assert "POST" in result
    assert "DELETE" in result


def test_render_html_custom_title():
    result = render_html(SAMPLE_ROUTES, title="My Custom API")
    assert "My Custom API" in result


# ── render dispatcher ────────────────────────────────────────────────────────

def test_render_dispatches_json():
    result = render(SAMPLE_ROUTES, fmt="json")
    assert json.loads(result)[0]["method"] == "GET"


def test_render_dispatches_text():
    result = render(SAMPLE_ROUTES, fmt="text")
    assert "GET" in result


def test_render_dispatches_html():
    result = render(SAMPLE_ROUTES, fmt="html")
    assert "<!DOCTYPE html>" in result


def test_render_case_insensitive_format():
    result = render(SAMPLE_ROUTES, fmt="JSON")
    assert json.loads(result) is not None


def test_render_unsupported_format_raises():
    with pytest.raises(ValueError, match="Unsupported format"):
        render(SAMPLE_ROUTES, fmt="xml")


def test_supported_formats_list():
    assert "json" in SUPPORTED_FORMATS
    assert "text" in SUPPORTED_FORMATS
    assert "html" in SUPPORTED_FORMATS
