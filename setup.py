#! /usr/bin/env python

from setuptools import setup, find_packages
import versioneer

setup (
    author = "J C Lawrence",
    author_email = "claw@kanga.nu",
    name = "xxpaper",
    cmdclass = versioneer.get_cmdclass (),
    include_package_data = True,
    install_requires = [line.strip ()
                        for line in open ("requirements.txt").readlines ()],
    long_description = "Tools for generating printable files of shares, privates, trains etc for 18xx and like games.",
    packages = find_packages (exclude = ["tests",]),
    version = versioneer.get_version (),
    zip_safe = False,
  )
