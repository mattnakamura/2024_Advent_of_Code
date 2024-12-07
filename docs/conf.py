"""Sphinx configuration."""

project = "2024_Advent_Of_Code"
author = "Matthew Nakamura"
copyright = "2024, Matthew Nakamura"
extensions = [
    "sphinx.ext.autodoc",
    "sphinx.ext.napoleon",
    "sphinxarg.ext",
    "myst_parser",
]
autodoc_typehints = "description"
html_theme = "furo"
