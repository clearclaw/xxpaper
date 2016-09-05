#! /usr/bin/env python

from setuptools import setup, find_packages
import versioneer

setup (
    name = "xxpaper",
    version = versioneer.get_version (),
    description = "Tools for generating files of 18xx papers.",
    long_description = "Tools for generating printable files of shares, privates, trains etc for 18xx and like games.",
    cmdclass = versioneer.get_cmdclass (),
    classifiers = [],
    keywords = "18xx, game files",
    author = "J C Lawrence",
    author_email = "claw@kanga.nu",
    url = "https://github.com/clearclaw/xxpaper",
    license = "GPL v3.0",
    packages = find_packages (exclude = ["tests",]),
    include_package_data = True,
    zip_safe = False,
    install_requires = [line.strip ()
                        for line in file ("requirements.txt").readlines ()
                    ] + ["psfile",],
  entry_points = {
    "console_scripts": [
      "xxpaper = xxpaper.main:main",
      ],
    },
  )
