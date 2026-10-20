from importlib.metadata import PackageNotFoundError, version

try:
    __version__ = version("wagtailstreamforms")
except PackageNotFoundError:  # pragma: no cover
    # running from a source checkout that was never installed
    __version__ = "0.0.0"
