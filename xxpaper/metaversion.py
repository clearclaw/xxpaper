#! /usr/bin/env python

"""
Uses `git describe` to dynamically generate a version for the
current code.  The version is effecvtively a traditional tri-tuple
ala (major, minor, patch), with the addenda that in this case the
patch string is a combination of the number of commits since the
tag, plus the ID of the last commit.  Further, the patch will be
extended with "-dirty" if there are uncommitted changes in the
current codeset.

  eg 1.0.1-gd5aa65e-dirty

Assumes that the tags fit the regex [0-9]*.[0-9]*
"""

import logging, pkg_resources, subprocess

LOG = logging.getLogger (__name__)
DEFAULT_GITCMD = "git describe --long --tags --match [0-9]*.[0-9]* --dirty"

def get_version ():
  try:
    o = subprocess.check_output (
      DEFAULT_GITCMD.split (),
      stderr = subprocess.PIPE,
      shell = False).decode ().strip ()
    s = o.replace ("-", ".", 1)
    return s, tuple (s.split ("."))
  except: # pylint: disable-msg=W0702
    # Likely not in a Git repo -- either way, punt
    s = pkg_resources.get_distribution (__name__.split (".")[0]).version
    return s, tuple (s.split ("."))
