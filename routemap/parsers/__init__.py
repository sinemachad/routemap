"""Route parsers for supported frameworks."""

from routemap.parsers.fastapi_parser import parse_file as parse_fastapi_file
from routemap.parsers.fastapi_parser import parse_directory as parse_fastapi_directory
from routemap.parsers.express_parser import parse_file as parse_express_file
from routemap.parsers.express_parser import parse_directory as parse_express_directory

SUPPORTED_FRAMEWORKS = ("fastapi", "express")


def get_parser(framework: str):
    """Return (parse_file, parse_directory) callables for the given framework."""
    framework = framework.lower()
    if framework == "fastapi":
        return parse_fastapi_file, parse_fastapi_directory
    elif framework == "express":
        return parse_express_file, parse_express_directory
    else:
        raise ValueError(
            f"Unsupported framework: '{framework}'. "
            f"Choose one of: {', '.join(SUPPORTED_FRAMEWORKS)}"
        )
