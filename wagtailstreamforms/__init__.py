from wagtailstreamforms.utils.version import get_version

# major.minor.patch.release.number
# release must be one of alpha, beta, rc, or final
VERSION = (3, 11, 0, "final", 1)

__version__ = get_version(VERSION)
