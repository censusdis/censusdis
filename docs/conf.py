# Configuration file for the Sphinx documentation builder.
#
# For the full list of built-in configuration values, see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

# -- Project information -----------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#project-information

import os
import sys

from typing import MutableMapping

sys.path.append(os.path.join(os.path.dirname(__file__), os.pardir))

def get_meta() -> MutableMapping:
    """Get project metadata from pyproject.toml file.
    Returns:
        MutableMapping
    """
    import toml

    toml_path = os.path.join(os.path.dirname(__file__), "..", "pyproject.toml")

    with open(toml_path) as fopen:
        pyproject = toml.load(fopen)

    return pyproject


meta = get_meta()

project = meta["tool"]["poetry"]["name"]
author = ",".join(meta["tool"]["poetry"]["authors"])
copyright = f"2022, {author}"
release = meta["tool"]["poetry"]["version"]

# -- General configuration ---------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#general-configuration

extensions = [
    "sphinx.ext.napoleon",
    "sphinx.ext.todo",
    "sphinx.ext.viewcode",
    "sphinx.ext.autodoc",
    "sphinx.ext.autosummary",
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

html_theme = "alabaster"
# html_theme = "sphinx_rtd_theme"

html_static_path = ["_static"]
