#! /usr/bin/env python

try:
  import pyver # pylint: disable=W0611
except ImportError:
  import os, subprocess
  try:
    environment = os.environ.copy()
    cmd = "pip install pyver".split (" ")
    subprocess.check_call (cmd, env = environment)
  except subprocess.CalledProcessError:
    import sys
    print >> sys.stderr, "Problem installing 'pyver' dependency."
    print >> sys.stderr, "Please install pyver manually."
    sys.exit (1)
  import pyver # pylint: disable=W0611

from setuptools import setup, find_packages

__version__, __version_info__ = pyver.get_version (pkg = "xxpaper",
                                                   public = True)

setup (name = "xxpaper",
  version = __version__,
  description = "Tools for generating images of 18xx papers.",
  long_description = "Tools for generating images of shares, privates, trains etc for 18xx and like games.",
  classifiers = [],
  keywords = "18xx, game files",
  author = "J C Lawrence",
  author_email = "claw@kanga.nu",
  url = "https://github.com/clearclaw/xxpaper",
  license = "Creative Commons Attribution-ShareAlike 3.0 Unported",
  packages = find_packages (exclude = ["tests",]),
  include_package_data = True,
  zip_safe = False,
  install_requires = [
    "configobj",
    "psfile",
    "pyver",
  ],
  entry_points = {
    "console_scripts": [
      "xxpaper = xxpaper.main:main",
      ],
    },
  )
