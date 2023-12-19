# Copyright (c) 2022-2023 Darren Erik Vengroff
"""
Tools for downloading and analyzing U.S. Census data.

Includes plotting maps and computing diversity and integration metrics.

Both Python and CLI interfaces are available.
"""
from .impl.exceptions import CensusApiException
import importlib.metadata
from pathlib import Path


def _package_version() -> str:
    """Find the version of the package."""
    package_version = "unknown"

    try:
        # Try to get the version of the current package if
        # it is running from a distribution.
        package = Path(__file__).parent.name
        metadata = importlib.metadata.metadata(package)

        package_version = metadata["Version"]
    except importlib.metadata.PackageNotFoundError:
        # Fall back on getting it from a local pyproject.toml.
        # This works in a development environment where the
        # package has not been installed from a distribution.
        import toml

        pyproject_toml_file = Path(__file__).parent.parent / "pyproject.toml"
        if pyproject_toml_file.exists() and pyproject_toml_file.is_file():
            package_version = toml.load(pyproject_toml_file)["tool"]["poetry"][
                "version"
            ]
            # Indicate it might be locally modified or unreleased.
            package_version = package_version + "+"

    return package_version


version = _package_version()

__all__ = ("CensusApiException", "version")
