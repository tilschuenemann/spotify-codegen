"""Sphinx configuration."""

project = "spotify-codegen"
author = "Til Schünemann"
copyright = "2022, Til Schünemann"
extensions = [
    "sphinx.ext.autodoc",
    "sphinx.ext.napoleon",
    "sphinx_click",
    "myst_parser",
    "sphinx_rtd_theme",
]
autodoc_typehints = "description"
html_theme = "sphinx_rtd_theme"
