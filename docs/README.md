# Wagtail Streamforms docs

These are Sphinx docs, automatically built when the master branch is committed to Github. To build them locally, from the repository root run:

    make docs

then open ``docs/_build/html/index.html`` in a browser.

To rebuild automatically while editing the documentation, from the repository root run:

    uv run --group docs sphinx-autobuild docs docs/_build/html

The online editor at http://rst.ninjs.org/ is a helpful tool for checking reStructuredText syntax.
