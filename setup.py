from setuptools import setup, find_packages

__version__ = "unknown"

exec open ("xxpaper/version.py")

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
  package_data = {
    'defaults': ['DEFAULT.conf',],
  },
  zip_safe = True,
  install_requires = [
    "configobj",
    "psfile",
  ],
  entry_points = {
    "console_scripts": [
      "xxpaper = xxpaper.main:main",
      ],
    },
  )
