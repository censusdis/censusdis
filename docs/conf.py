# Configuration file for the Sphinx documentation builder.
#
# For the full list of built-in configuration values, see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

# -- Project information -----------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#project-information

import os
import sys
from typing import MutableMapping

import mock

# We have to mock out certain modules that are not pure
# python because RTD will not import them.
MOCK_MODULES = [
    "geopandas",
    "matplotlib",
    "matplotlib.pyplot",
    "pandas",
    "numpy",
    "scipy",
    "shapely",
    "shapely.affinity",
    "shapely.geometry",
    "shapely.geometry.base",
    "rtree",
]

for mod_name in MOCK_MODULES:
    sys.modules[mod_name] = mock.Mock()

# This is where the source we want to document lives.
SRC_ROOT = os.path.join(os.path.dirname(__file__), os.pardir)
sys.path.append(SRC_ROOT)


def get_pyproject() -> MutableMapping:
    """
    Get project metadata from pyproject.toml file.

    Returns:
        MutableMapping
    """
    import toml

    toml_path = os.path.join(os.path.dirname(__file__), os.pardir, "pyproject.toml")

    with open(toml_path) as fopen:
        pyproject = toml.load(fopen)

    return pyproject


pyproject = get_pyproject()

project = pyproject["tool"]["poetry"]["name"]
author = ",".join(pyproject["tool"]["poetry"]["authors"])
copyright = f"2022, {author}"
release = pyproject["tool"]["poetry"]["version"]

# -- General configuration ---------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#general-configuration

extensions = [
    "sphinx.ext.napoleon",
    "sphinx.ext.todo",
    "sphinx.ext.viewcode",
    "sphinx.ext.autodoc",
    "sphinx.ext.autosummary",
    "nbsphinx",
]

# copybutton config
copybutton_prompt_text = r">>> |\.\.\. |\$ "
copybutton_prompt_is_regexp = True

# autodoc config
autodoc_default_options = {
    "autosummary": True,
}

templates_path = ["_templates"]
exclude_patterns = ["_build", "Thumbs.db", ".DS_Store"]


# -- Options for HTML output -------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#options-for-html-output

html_theme = "sphinx_rtd_theme"

html_static_path = ["_static"]
