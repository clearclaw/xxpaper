from setuptools import setup, find_packages

__version__ = "unknown"

import pyver
__version__, __version_info__ = pyver.get_version (pkg = "xxpaper", public = True)

setup (name = "xxpaper",
  version = __version__,
  description = "Tools for generating images of 18xx papers.",
  long_description = "Tools for generating images of shares, privates, trains etc for 18xx and like games.",
  classifiers = [],
  keywords = "",
  author = "J C Lawrence",
  author_email = "claw@kanga.nu",
  url = "http://kanga.nu/~claw/",
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
