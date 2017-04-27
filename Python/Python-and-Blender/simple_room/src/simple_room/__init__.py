# -*- test-case-named: simple_room -*-

"""
simple_room: A simple room.
"""

def _checkRequirements():
    import sys

    version = getattr(sys, "version_info", (0,))
    if version < (2, 7):
        raise ImportError("Simple_room requires Python 2.7 or later.")
    elif version >= (3, 0) and version < (3, 3):
        raise ImportError("Simple_Room requires Python 3.3 or later.")

_checkRequirements()

# setup version
from simple_room._version import __version__ as version
__version__ = version.short()
