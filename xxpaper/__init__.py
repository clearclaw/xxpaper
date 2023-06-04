#! /usr/bin/env python

from . import _version
__version__ = _version.get_versions()['version']
__version_info__ = _version.get_versions ()
del _version

from . import cmds
