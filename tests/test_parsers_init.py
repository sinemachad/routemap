import pytest
from routemap.parsers import get_parser, SUPPORTED_FRAMEWORKS
from routemap.parsers.fastapi_parser import parse_file as fastapi_pf, parse_directory as fastapi_pd
from routemap.parsers.express_parser import parse_file as express_pf, parse_directory as express_pd


def test_supported_frameworks_contains_fastapi():
    assert "fastapi" in SUPPORTED_FRAMEWORKS


def test_supported_frameworks_contains_express():
    assert "express" in SUPPORTED_FRAMEWORKS


def test_get_parser_fastapi():
    pf, pd = get_parser("fastapi")
    assert pf is fastapi_pf
    assert pd is fastapi_pd


def test_get_parser_express():
    pf, pd = get_parser("express")
    assert pf is express_pf
    assert pd is express_pd


def test_get_parser_case_insensitive():
    pf, pd = get_parser("FastAPI")
    assert pf is fastapi_pf

    pf, pd = get_parser("Express")
    assert pf is express_pf


def test_get_parser_unsupported_raises():
    with pytest.raises(ValueError, match="Unsupported framework"):
        get_parser("django")


def test_get_parser_unsupported_message_includes_supported():
    with pytest.raises(ValueError, match="fastapi"):
        get_parser("rails")
