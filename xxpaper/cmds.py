#! /usr/bin/env python

from __future__ import absolute_import
import clip, logging, logtool
from .main import app_main

LOG = logging.getLogger (__name__)
OPTIONS = ["help", "debug", "nosentry", "verbose", "version"]

@app_main.subcommand (
  name = "check",
  description = "Check formatting of game file",
  inherits = OPTIONS)
@clip.arg (name = "template", default = None,
           help = "XXPaper game file", required = True)
@logtool.log_call
def check (**kwargs):
  from .cmd_check import do
  do (**kwargs)

@app_main.subcommand (
  name = "dump",
  description = "Dump the compiled game definition",
  inherits = OPTIONS)
@clip.arg (name = "templates", default = None,
           help = "XXPaper game files (comma separated)", required = True)
@clip.opt ("-o", "--output", name = "output", default = "yaml",
           help = "Output format", required = False)
@logtool.log_call
def dump (**kwargs):
  from .cmd_dump import do
  do (**kwargs)

@app_main.subcommand (
  name = "lookup",
  description = "Check the value of a key",
  inherits = OPTIONS)
@clip.arg (name = "templates",
           help = "XXPaper game files (comma separated)", required = True)
@clip.arg (name = "typ", required = True, help = "Typ to search")
@clip.arg (name = "name", required = True, help = "name to search")
@clip.arg (name = "n", required = True, help = "Number to search")
@clip.arg (name = "key",
           help = "Key to evaluate)", required = True)
@logtool.log_call
def lookup (**kwargs):
  from .cmd_lookup import do
  do (**kwargs)

@app_main.subcommand (
  name = "make",
  description = "Make artfile for a game",
  inherits = OPTIONS)
@clip.flag ("-c", "--cutline", name = "cutline",
            default = False, help = "Draw cutlines")
@clip.opt ("-f", "--filter", name = "filter",
           help = "Only these asset-types")
@clip.opt ("-p", "--paper", name = "paper",
           default = "A4", help = "Paper size (A4, letter)")
@clip.opt ("-r", "--repeat", name = "repeat",
           default = "", help = "Make repeats of these (comma separated)")
@clip.arg (name = "templates",
           help = "XXPaper game files (comma separated)", required = True)
@clip.arg (name = "outfile",
           help = "File to produce (default: first template .pdf)",
           required = False)
@logtool.log_call
def make (**kwargs):
  from .cmd_make import do
  do (**kwargs)
